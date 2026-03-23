import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


from grain_growth import GrainSimulation 

# --- PAGE CONFIG ---
st.set_page_config(page_title="Grain Growth ICME", layout="wide")
st.title("🧪 Microstructure Generator (ICME)")
st.markdown("Web interface for generating synthetic microstructure.")

# --- SIDEBAR (SETTINGS) ---
st.sidebar.header("Grid Parameters")
length = st.sidebar.slider("Length", 50, 1000, 150)
width = st.sidebar.slider("Width", 50, 1000, 150)
num_grains = st.sidebar.slider("Initial Grains", 1, 300, 30)
pbc = st.sidebar.checkbox("Periodic Boundary Conditions (PBC)", value=False)

st.sidebar.header("Physics Parameters")
mobility = st.sidebar.slider("Boundary Mobility (Temp)", 0.01, 1.0, 1.0, step=0.05)
pinning = st.sidebar.slider("Nanopores Fraction (Pinning)", 0.0, 0.5, 0.0)
nucl_rate = st.sidebar.slider("Continuous Nucleation (JMAK)", 0, 10, 0)

st.sidebar.header("Output Settings")
output_mode = st.sidebar.radio("Visualization Mode", ["Animation (GIF)", "Static Image (PNG)"])

# --- MAIN SCREEN ---
if st.button("🚀 Generate Microstructure", type="primary"):
    
    with st.spinner("Calculating tensors and rendering... Please wait."):
        
        # 1. Initialize the physical engine
        sim = GrainSimulation(
            length=length, 
            width=width, 
            num_grains=num_grains, 
            pbc=pbc, 
            nucl_rate=nucl_rate, 
            pinning=pinning,
            mobility=mobility
        )
        
        # 2. Logic for Animation (GIF)
        if output_mode == "Animation (GIF)":
            gif_filename = "ui_result.gif"
            sim.save_gif(gif_filename)
            
            st.success("✅ Simulation completed successfully!")
            st.image(gif_filename, caption="Crystallization Process", use_container_width=True)
            
        # 3. Logic for Static Image (PNG)
        else:
            # Run the mathematical evolution silently until the grid is filled
            while 0 in sim.field_matr:
                sim.evol_step_vectorized()
            
            # Prepare the visual matrix (same logic as in your display method)
            fig, ax = plt.subplots()
            vis_matr = np.where(sim.field_matr == 0, 0, (sim.field_matr % 1000) + 1)
            
            # Apply the black mask for nanopores if pinning is used
            if sim.pinning > 0:
                vis_matr = np.ma.masked_where(sim.field_matr == -1, vis_matr)
                
            ax.imshow(vis_matr, cmap=sim.my_cmap, vmin=0.5, vmax=1000.5)
            ax.axis('off') # Hide the axis numbers for a cleaner look
            
            st.success("✅ Simulation completed successfully!")
            st.pyplot(fig) # Render the matplotlib figure directly in Streamlit!import streamlit as st

