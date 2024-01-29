import cohere
import streamlit as st

# Initialize Cohere client with a placeholder key
co = cohere.Client('placeholder-key')

def generate_recipe(cuisine_type, creativity):
    """
    Generate a recipe idea given a cuisine type.
    Arguments:
    cuisine_type(str): the type of cuisine
    creativity(float): the Generate model `temperature` value
    Returns:
    response(str): the recipe idea
    """
    recipe_prompt = f"""Generate a recipe idea given the cuisine type. Here are a few examples.

--
Cuisine Type: Italian
Recipe Idea: A twist on classic spaghetti carbonara using zucchini noodles and turkey bacon

--
Cuisine Type: Mexican
Recipe Idea: Vegetarian enchiladas with a homemade tomato sauce and a mix of grilled vegetables

--
Cuisine Type: Indian
Recipe Idea: Slow-cooked chicken tikka masala with coconut milk and a blend of traditional spices

--
Cuisine Type: Chinese
Recipe Idea: Stir-fried tofu with broccoli and a spicy Szechuan sauce

--
Cuisine Type: {cuisine_type}
Recipe Idea: """

    # Assuming the use of a hypothetical 'co.generate' function similar to the original code
    response = co.generate(
        model="command",
        prompt=recipe_prompt,
        max_tokens=50,
        temperature=creativity,
        k=0,
        stop_sequences=["--"],
    )
    recipe_idea = response.generations[0].text
    print(recipe_prompt)
    print("recipe_idea - pre", recipe_idea)
    recipe_idea = recipe_idea.replace("\n\n--", "").replace("\n--", "").strip()
    print("recipe_idea - post", recipe_idea)
    print("-------------")
    return recipe_idea


# Frontend: Title and API Key Input
st.title("🍳 Recipe Suggestion Generator")
api_key = st.text_input("Enter your Cohere API key", type="password")

if api_key:
    # Update the Cohere client with the actual API key
    co = cohere.Client(api_key)
    st.success("API Key accepted!")

# Recipe Form
form = st.form(key="user_settings")
with form:
    # User input - Industry name
    cusine_input = st.text_input("Cusine type")

    # Create a two-column view
    col1, col2 = st.columns(2)
    with col1:
        # User input - The number of cusines to generate
        num_input = st.slider(
            "Number of ideas",
            value=3,
            key="num_input",
            min_value=1,
            max_value=10,
            help="Choose to generate between 1 to 10 ideas",
        )
    with col2:
        # User input - The 'temperature' value representing the level of creativity
        creativity_input = st.slider(
            "Creativity",
            value=0.5,
            key="creativity_input",
            min_value=0.1,
            max_value=0.9,
            help="Lower values generate more “predictable” output, higher values generate more “creative” output",
        )
    # Submit button to start generating ideas
    generate_button = form.form_submit_button("Generate Idea")

    if generate_button:
        if cusine_input == "":
            st.error("cusine field cannot be blank")
        else:
            my_bar = st.progress(0.05)
            st.subheader("Recipe generator:")

        for i in range(num_input):
            st.markdown("""---""")
            recipe_suggestion = generate_recipe(cusine_input, creativity_input)
            st.markdown("##### Recipe Suggestion")
            st.write(recipe_suggestion)
            my_bar.progress((i + 1) / num_input)
