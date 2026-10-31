from google import genai
from PIL import Image
import streamlit as st

# Configuration de la page
st.set_page_config(page_title="CookAi 🍳", page_icon="🍳", layout="centered")

st.title("🍳 CookAi - Ton Chef Intelligent")
st.write(
    "Importe une photo de ton frigo, prends-en une en direct, ou écris tes"
    " ingrédients !"
)

# Option 1 : Importer une image depuis l'ordinateur ou le téléphone
uploaded_file = st.file_uploader(
    "📁 Importer une photo d'ingrédients", type=["jpg", "jpeg", "png"]
)

# Option 2 : Ou utiliser la caméra en direct
camera_image = st.camera_input("📸 Ou prends une photo en direct")

# Option 3 : Écrire les ingrédients au clavier
ingredients_text = st.text_input(
    "✍️ Ou écris tes ingrédients (ex: tomates, œufs, oignons)"
)

# Initialisation du client GenAI avec ta clé API
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if st.button("Trouver des recettes de chef 🍽️"):
    # On vérifie qu'on a bien soit une image, soit du texte
    if uploaded_file is not None or camera_image is not None or ingredients_text:
        with st.spinner(
            "CookAi analyse les ingrédients et mijote de superbes idées..."
        ):
            try:
                contents = []
                pil_image = None

                # Récupération de l'image selon la source (Upload ou Caméra) et conversion avec PIL
                if uploaded_file is not None:
                    pil_image = Image.open(uploaded_file)
                elif camera_image is not None:
                    pil_image = Image.open(camera_image)

                # Si on a une image, on l'ajoute proprement avec le texte
                if pil_image is not None:
                    prompt_text = (
                        "Regarde cette photo de mes ingrédients. Agis comme un"
                        " chef cuisinier créatif. Propose 2 ou 3 recettes simples"
                        " et délicieuses avec ce que tu vois. Donne un nom"
                        " sympa, la liste des ingrédients et les étapes de"
                        " préparation rapides."
                    )
                    contents = [pil_image, prompt_text]
                else:
                    # Si on a seulement du texte
                    contents = (
                        f"Agis comme un chef cuisinier créatif et pragmatique. À"
                        f" partir de ces ingrédients : {ingredients_text},"
                        " propose 2 ou 3 recettes simples et délicieuses. Donne"
                        " un nom sympa, la liste des ingrédients et les étapes"
                        " de préparation rapides."
                    )

                # Appel à l'API Gemini avec un modèle flash stable et supporté
                response = client.models.generate_content(
                    model="gemini-2.5-flash", contents=contents
                )

                # Affichage du résultat
                st.success("Voici tes idées de recettes personnalisées !")
                st.markdown(response.text)

            except Exception as e:
                st.error(
                    "Une erreur est survenue lors de la communication avec"
                    f" l'API Gemini :\n`{e}`"
                )
    else:
        st.warning(
            "Oups ! Importe une photo, prends-en une ou écris quelques"
            " ingrédients d'abord."
        )