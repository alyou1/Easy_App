import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Formulaire Multi-pages", page_icon="📝")

# Initialisation de la session state pour gérer les pages
if 'page' not in st.session_state:
    st.session_state.page = 1

# Initialisation des données du formulaire
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Fonction pour passer à la page suivante
def next_page():
    st.session_state.page += 1

# Fonction pour revenir à la page précédente
def prev_page():
    st.session_state.page -= 1

# Fonction pour terminer le formulaire
def finish_form():
    st.session_state.completed = True

# En-tête
st.title("📝 Formulaire Multi-pages")
st.progress((st.session_state.page - 1) / 2)

# PAGE 1
if st.session_state.page == 1:
    st.header("Page 1 - Informations personnelles")
    
    with st.form("page1_form"):
        nom = st.text_input("Nom", value=st.session_state.form_data.get('nom', ''))
        prenom = st.text_input("Prénom", value=st.session_state.form_data.get('prenom', ''))
        email = st.text_input("Email", value=st.session_state.form_data.get('email', ''))
        telephone = st.text_input("Téléphone", value=st.session_state.form_data.get('telephone', ''))
        
        submitted = st.form_submit_button("Suivant ➡️")
        
        if submitted:
            # Sauvegarder les données
            st.session_state.form_data['nom'] = nom
            st.session_state.form_data['prenom'] = prenom
            st.session_state.form_data['email'] = email
            st.session_state.form_data['telephone'] = telephone
            next_page()
            st.rerun()

# PAGE 2
elif st.session_state.page == 2:
    st.header("Page 2 - Informations complémentaires")
    
    with st.form("page2_form"):
        adresse = st.text_area("Adresse", value=st.session_state.form_data.get('adresse', ''))
        ville = st.text_input("Ville", value=st.session_state.form_data.get('ville', ''))
        code_postal = st.text_input("Code postal", value=st.session_state.form_data.get('code_postal', ''))
        commentaires = st.text_area("Commentaires (optionnel)", value=st.session_state.form_data.get('commentaires', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("⬅️ Retour")
        with col2:
            submitted = st.form_submit_button("Terminer ✅")
        
        if back:
            prev_page()
            st.rerun()
        
        if submitted:
            # Sauvegarder les données
            st.session_state.form_data['adresse'] = adresse
            st.session_state.form_data['ville'] = ville
            st.session_state.form_data['code_postal'] = code_postal
            st.session_state.form_data['commentaires'] = commentaires
            finish_form()
            st.rerun()

# PAGE DE CONFIRMATION
if 'completed' in st.session_state and st.session_state.completed:
    st.success("✅ Formulaire soumis avec succès !")
    st.balloons()
    
    st.subheader("Récapitulatif de vos informations :")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Informations personnelles**")
        st.write(f"Nom: {st.session_state.form_data.get('nom', '')}")
        st.write(f"Prénom: {st.session_state.form_data.get('prenom', '')}")
        st.write(f"Email: {st.session_state.form_data.get('email', '')}")
        st.write(f"Téléphone: {st.session_state.form_data.get('telephone', '')}")
    
    with col2:
        st.write("**Informations complémentaires**")
        st.write(f"Adresse: {st.session_state.form_data.get('adresse', '')}")
        st.write(f"Ville: {st.session_state.form_data.get('ville', '')}")
        st.write(f"Code postal: {st.session_state.form_data.get('code_postal', '')}")
        st.write(f"Commentaires: {st.session_state.form_data.get('commentaires', 'Aucun')}")
    
    if st.button("Nouveau formulaire"):
        # Réinitialiser tout
        st.session_state.page = 1
        st.session_state.form_data = {}
        del st.session_state.completed
        st.rerun()
