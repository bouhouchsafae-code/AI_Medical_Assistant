import cloudinary
import cloudinary.uploader

# =========================
# ☁️ CLOUDINARY CONFIG
# =========================

cloudinary.config(

    cloud_name="drgvdxxtr",

    api_key="368149539189523",

    api_secret="LQusW02UCONbAuD563aLaQhw1Zo"

)

# =========================
# 📤 Upload Image
# =========================

def upload_image(

    file,
    folder="medical_ai"

):

    result = cloudinary.uploader.upload(

        file,

        folder=folder

    )

    return result["secure_url"]