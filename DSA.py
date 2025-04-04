import streamlit as st
import google.generativeai as genai
import openai
import os
import time
import subprocess

genai.configure(api_key="")
model = genai.GenerativeModel('gemini-1.5-flash-latest')

openai.api_key = ""

# Enhanced Custom CSS Styling with Gradient Background
page_bg_img = '''
<style>
body {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    background-size: cover;
    background-attachment: fixed;
    color: #1A374D;
}

textarea, input {
    background-color: #FFFFFF;
    border-radius: 8px;
    padding: 10px;
}

button {
    background-color: #F2545B;
    color: #FFFFFF;
    border-radius: 8px;
    padding: 8px 16px;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
# Generate Manim Video
def generate_manim_video(manim_code, video_class_name="MathExplanation"):
    timestamp = int(time.time())
    script_path = f"{video_class_name}_{timestamp}.py"

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(manim_code)

    subprocess.run(["manim", "--clear-cache"])
    subprocess.run(["manim", "-ql", script_path, video_class_name])

    video_dir = f"media/videos/{video_class_name}_{timestamp}/480p15"

    if not os.path.exists(video_dir):
        st.error(f"⚠️ Video directory does not exist: {video_dir}")
        return None

    video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
    if not video_files:
        st.error(f"⚠️ No MP4 files found in: {video_dir}")
        return None

    video_files.sort(key=lambda x: os.path.getmtime(os.path.join(video_dir, x)), reverse=True)
    video_path = os.path.join(video_dir, video_files[0])

    st.write(f"✅ Video generated successfully: {video_path}")
    return video_path


# Generate Manim Code
def generate_script(algo):
    prompt = f"Explain this algorithm step by step with clear explanation. {algo}"
    response = model.generate_content(prompt)
    
    if response and hasattr(response, 'text'):
        st.session_state.solution_text = response.text
        return response.text
    else:
        return "Sorry, I couldn't generate the content."


# Generate Manim Prompt for code generation
def generate_manim_prompt(algorithm):
    return f"""
Generate a Manim animation that visually explains the {algorithm} algorithm.
Use shapes, animations, and text to break down the process step-by-step.
Ensure all variables and transitions are clearly displayed.
Use MathTex for all numerical representations.
Avoid overlapping mobjects and use TransformMatchingTex where necessary.
"""


# Sidebar Menu
st.sidebar.header("CODE-GEN")
menu_choice = st.sidebar.radio("Select a Feature", ["DSA-TOPICS", "ADVANCED-FEATURES", "CONTEST-TRAINER"], key="menu_type")

dsa_topics = {
    "SORTING & SEARCHING": ["Binary Search", "Merge Sort", "Quick Sort"],
    "ARRAY": ["Kadane's Algorithm", "Two-Pointer Technique", "Sliding Window", "Prefix Sum"],
    "LINKED LIST": ["Floyd’s Cycle-Finding Algorithm", "Reverse a Linked List", "Merge Sort in Linked List"],
    "STACK": ["Balanced Parenthesis", "Next Greater Element", "Stock Span Problem"],
    "QUEUE": ["Circular Queue", "Deque", "Sliding Window Maximum"],
    "HASHING": ["Hash Tables", "Hash Maps", "Anagram Checking"],
    "TREE": ["Binary Search Tree", "AVL Tree", "Tree Traversals"],
    "GRAPH": ["DFS", "BFS", "Dijkstra's Algorithm"],
    "HEAP": ["Min-Heap", "Max-Heap", "Heap Sort"],
    "TRIE": ["Prefix Matching", "Autocomplete", "Longest Common Prefix"],
    "DYNAMIC PROGRAMMING": ["0/1 Knapsack", "Longest Increasing Subsequence", "Fibonacci"],
    "GREEDY ALGORITHM": ["Activity Selection", "Fractional Knapsack", "Job Sequencing"],
    "BACKTRACKING": ["N-Queens", "Sudoku Solver", "Subset Sum"],
    "BIT MANIPULATION": ["Bitmasking", "XOR Tricks", "Power of Two Checking"]
}
def show_dsa_topics():

        if menu_choice == "DSA-TOPICS":
            st.header("📚 Learn DSA Topics")
            selected_topic = st.sidebar.selectbox("Select DSA Topic", list(dsa_topics.keys()))
            
            if selected_topic:
                st.header(f"📖 Learn {selected_topic}")
                selected_algorithm = st.selectbox("Choose an algorithm", dsa_topics[selected_topic])

                if st.button("GENERATE"):
                    content = generate_script(selected_algorithm)
                    st.write(content)
                st.session_state.video_generated = False  
                    
                prompt_Manim = (
                    f"""Generate a complete Manim script using Python that visually explains the concepts{generate_script(selected_algorithm)}.  The script should:

                    1. Include clear alignment of text and visuals without overlapping.
                    2. Set proper time delays and timeouts for animations to provide a smooth learning experience.
                    3. Display text, code explanations, diagrams, and animations in a structured way.
                    4. Ensure animations are well-timed and not rushed.
                    5. Provide only the code response. No additional text or explanation.

                    there are some error you need to avoid(Important):
                    1. Attribute Errors
                        AttributeError: 'Scene' object has no attribute 'begin_ambient_camera_rotation'
                        AttributeError: 'Text' object has no attribute 'set_color'
                        AttributeError: 'NumberPlane' object has no attribute 'scale'
                        AttributeError: 'Group' object has no attribute 'add_updater'
                        AttributeError: 'ThreeDScene' object has no attribute 'wait'
                        AttributeError: 'OpenGLVMobject' object has no attribute 'generate_target'
                        AttributeError: 'Tex' object has no attribute 'next_to'
                        AttributeError: 'Graph' object has no attribute 'animate'
                        AttributeError: 'VolumeOfSphere' object has no attribute 'set_fill'
                        AttributeError: 'FadeIn' object has no attribute 'set_opacity'
                    2. Value Errors
                        ValueError: Cannot set color for Mobject without stroke
                        ValueError: Unknown color name 'rainbow'
                        ValueError: Cannot set fill color for a VMobject
                        ValueError: Interpolation failed due to NaN values
                        ValueError: Points array cannot be empty
                        ValueError: latex error converting to dvi. See log output above
                        ValueError: Invalid dimension for matrix
                        ValueError: Cannot animate non-Mobject type
                        ValueError: Number of anchors must match the number of control points
                        ValueError: Path cannot be created with zero-length vectors
                    3. Import Errors
                        ImportError: No module named 'manim'
                        ImportError: cannot import name 'ShowCreation' from 'manim'
                        ImportError: cannot import name 'Graph' from 'manim.mobject.graph'
                        ImportError: cannot import name 'TransformMatchingShapes'
                        ImportError: DLL load failed while importing cairo
                        ImportError: cannot import name 'ThreeDScene'
                        ImportError: cannot import name 'MathTex'
                        ImportError: cannot import name 'DashedVMobject'
                        ImportError: No module named 'manim.opengl'
                        ImportError: cannot import name 'Surface' from 'manim.mobject'
                    4. Type Errors
                        TypeError: Object of type 'Circle' has no len()
                        TypeError: 'int' object is not callable
                        TypeError: 'float' object is not iterable
                        TypeError: 'NoneType' object is not iterable
                        TypeError: expected str, bytes or os.PathLike object, not PosixPath
                        TypeError: unsupported operand type(s) for +: 'VMobject' and 'int'
                        TypeError: 'list' object is not callable
                        TypeError: cannot unpack non-iterable int object
                        TypeError: Missing required positional argument 'file_path'
                        TypeError: Object is not JSON serializable
                    5. Rendering Errors
                        RuntimeError: Cairo surface not properly initialized
                        RuntimeError: FFmpeg process returned non-zero exit code
                        RuntimeError: Shader compilation failed
                        RuntimeError: Could not open video file
                        RuntimeError: Cannot animate object with no animations
                        RuntimeError: ManimGL not found
                        RuntimeError: No output file created
                        RuntimeError: Object has been deleted before rendering
                        RuntimeError: Could not locate Tex output
                        RuntimeError: LaTeX process crashed
                    6. LaTeX Errors
                        ValueError: LaTeX failed to compile. Check your installation.
                        ValueError: Invalid TeX command
                        ValueError: Cannot create MathTex from empty string
                        ValueError: Undefined control sequence in LaTeX
                        ValueError: LaTeX file could not be generated
                        ValueError: Missing dollar signs in inline equation
                        ValueError: Extra brace detected in LaTeX string
                        ValueError: Unknown package 'amsmath'
                        ValueError: Overfull hbox detected
                        ValueError: LaTeX source file is empty
                    7. Camera & Scene Errors
                        AttributeError: 'ThreeDScene' object has no attribute 'set_camera_orientation'
                        ValueError: Invalid zoom level for camera
                        RuntimeError: Cannot rotate camera before initialization
                        ValueError: Cannot add ambient light in a 2D scene
                        IndexError: List index out of range while setting camera path
                        AttributeError: 'Camera' object has no attribute 'save_state'
                        RuntimeError: Cannot animate camera before scene is played
                        TypeError: Cannot assign NoneType to camera rotation
                        ValueError: Camera target must be a Mobject
                        RuntimeError: Camera cannot capture empty scene
                    8. Animation Errors
                        AttributeError: 'FadeIn' object has no attribute 'play'
                        ValueError: Animation requires at least one frame
                        RuntimeError: Cannot animate removed object
                        TypeError: Animation duration must be a number
                        ValueError: Cannot animate an empty list of Mobjects
                        RuntimeError: Too many nested animations
                        AttributeError: 'Transform' object has no attribute 'update'
                        IndexError: Animation list index out of range
                        RuntimeError: Mobject must be added to scene before animating
                        ValueError: Animation target cannot be None
                    9. File & Path Errors
                        FileNotFoundError: No such file or directory
                        PermissionError: Cannot write to directory
                        OSError: Could not create video file
                        ValueError: Invalid file extension
                        FileNotFoundError: FFmpeg binary not found
                        RuntimeError: Temporary directory could not be created
                        OSError: Disk full while saving output
                        ValueError: Cannot save Mobject to file
                        OSError: File already exists
                        FileNotFoundError: Required asset missing
                    10. OpenGL Errors
                        RuntimeError: OpenGL context not found
                        ValueError: Cannot use OpenGL mode in software rendering
                        AttributeError: 'GLScene' object has no attribute 'set_background'
                        RuntimeError: Shader compilation error
                        ValueError: Cannot render OpenGL object in CPU mode
                        RuntimeError: Framebuffer object creation failed
                        AttributeError: OpenGL buffer has no attribute 'bind'
                        RuntimeError: OpenGL version mismatch
                        TypeError: OpenGL Mobject requires vector input
                        ValueError: Invalid OpenGL vertex format

                    
                    """
                )
            
                try:
                    response = openai.chat.completions.create(
                        model="gpt-4.5-preview",
                        messages=[
                            {"role": "system", "content": "You are a Manim code creator for version [0.19.0]."},
                            {"role": "user", "content": prompt_Manim}
                        ]
                    )

                    # To extract the generated message from the response
                    manim_code = response.choices[0].message.content

                    
                    # Process the generated Manim script
                    manim_script_lines = manim_code.split('\n')
                    
                    # Remove code block markers if they exist
                    if manim_script_lines[0].strip() == "```python":
                        manim_script_lines = manim_script_lines[1:]
                    if manim_script_lines[-1].strip() == "```":
                        manim_script_lines = manim_script_lines[:-1]
                    
                    # Cleaned script
                    cleaned_manim_script = "\n".join(manim_script_lines)
                    
                    # Save cleaned script to session state
                    st.session_state.manim_script = cleaned_manim_script
                    st.write("✅ Manim Code Generated Successfully!")

                except Exception as e:
                    st.write(f"❌ Failed to generate Manim Code. Error: {e}")

        # Display generated code if available
        if st.session_state.manim_script:
            st.text_area("Generated Manim Code", st.session_state.manim_script, height=300)
            
            if st.button("Generate Video Explanation"):
                st.session_state.video_generated = True


        if st.session_state.video_generated:
            with st.spinner("🎥 Generating video..."):
                try:
                    video_path = generate_manim_video(st.session_state.manim_script)
                
                    
                    if video_path:
                        st.video(video_path)
                        st.success("✅ Video generated successfully with narration!")
                    else:
                        st.error("❌ Failed to generate the video.")
                except Exception as e:
                    st.error(f"⚠️ Error generating video: {e}")

                        
def generate_manim_prompt(algorithm):
    """
    Generates a structured prompt for Manim animation generation.

    Args:
        algorithm (str): The algorithm or operation to illustrate.
        data_structure (str): The data structure involved.
        initial_state (str): A string representing the initial state of the data structure.
        title (str): The title of the animation.

    Returns:
        str: A structured prompt for Manim.
    """

    prompt_manim = f"""
Generate a Manim animation illustrating the {algorithm} operation on a data_structure with the following initial state:


Show each step of the operation clearly using appropriate Manim objects (e.g., rectangles, circles, arrows, lines).

Use MathTex for all numerical values, variable updates, and data structure element representations.

Include a title  at the top of the scene.

Use Code objects to display python code if any.

Do not use plain text for variable assignments.

Do not use mobjects that overlap each other.

If there is a need to show a variable change, use TransformMatchingTex.

If any error occurs, generate a simple animation that displays the message 'Error during animation generation.'
"""
    return prompt_manim
def show_advanced_features():
    st.header("Advanced Features")
    advanced_options = ["VIDEO-GEN","INTUITION", "BUG-FIXING", "SOLVING"]
    selected_advanced = st.sidebar.radio("Select Advanced Feature", advanced_options, key="advanced_menu")

    if selected_advanced == "INTUITION":
        st.header("INTUITION")
        problem = st.text_area("Describe your problem to understand the intuition behind it")
        if st.button("IQ+++"):
            prompt = f"GIVE INTUTION TO SOLVE THIS PROBLEM AND HOW TO APPROACH THIS CODING PROBLEM AND ONE IMPORTANT MAIN THING IS DO NOT PROVIDE THE CODE TELL ONLY THE INTUTION:{problem}"
            response = model.generate_content(prompt + problem)
            st.session_state.solution_text = response.text
            st.write(st.session_state.solution_text)

    elif selected_advanced == "BUG-FIXING":
        st.header("BUG-FIXING")
        code_snippet = st.text_area("Paste your code snippet for bug-fixing")
        if st.button("bug it"):
            prompt = f"CORRECT THE CODE AND EXPLAIN WHERE I MADE THE ERROR TRY TO DEBUG :{code_snippet}"
            response = model.generate_content(prompt + code_snippet)
            st.session_state.solution_text = response.text
            st.write(st.session_state.solution_text)

    elif selected_advanced == "VIDEO-GEN":
        st.header("🎥 Generate Video")
        algorithm = st.text_area("Describe your problem to understand the intuition behind it")
        st.session_state.video_generated = False  
        prompt = generate_manim_prompt(algorithm)

        response = model.generate_content(prompt + algorithm)
        st.session_state.solution_text = response.text
    
    # Store the response in Streamlit's session state
        # Extracting the text response from the model
        raw_manim_script = response.text.strip() if hasattr(response, 'text') else response.strip()
        manim_script_lines = raw_manim_script.split('\n')

        # Remove code block markers if they exist
        if manim_script_lines[0] == "```python":
            manim_script_lines = manim_script_lines[1:]

        if manim_script_lines[-1] == "```":
            manim_script_lines = manim_script_lines[:-1]

        # Join the lines back into a single script
        cleaned_manim_script = "\n".join(manim_script_lines)

        # Save cleaned script to session state
        st.session_state.manim_script = cleaned_manim_script

        if st.session_state.manim_script:
            if st.button("Generate Video Explanation"):
                st.session_state.video_generated = True  

        if st.session_state.video_generated:
            with st.spinner("Generating video..."):
                try:
                    video_path = generate_manim_video(st.session_state.manim_script)
                    st.video(video_path)
                    st.success("Video generated successfully!")
                except Exception as e:
                    st.error(f"Error generating video: {e}")

    elif selected_advanced == "SOLVING":
        st.header("📝 SOLVING")
        problem_statement = st.text_area("Describe your coding problem")
        if st.button("SOLVE IT"):
            prompt = f"GIVE SOLUTION CODE FOR THIS (LEETCODE, CODE CHEF, HACKER RANK, CODE FORCE, ETC..) FOR  THIS PROBLEM AND EXPLAIN THE LINE STEP BY STEP:{problem_statement}"
            response = model.generate_content(prompt + problem_statement)
            st.session_state.solution_text = response.text
            st.write(st.session_state.solution_text)

def show_contest_trainer():
    st.header("Contest Trainer")
    st.write("Contest Training Functionality Coming Soon!")


if menu_choice == "DSA-TOPICS":
    show_dsa_topics()
elif menu_choice == "ADVANCED-FEATURES":
    show_advanced_features()
elif menu_choice == "CONTEST-TRAINER":
    show_contest_trainer()
