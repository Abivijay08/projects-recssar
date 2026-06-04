import streamlit as st
import requests

# -----------------------
# PAGE CONFIG
# -----------------------

st.set_page_config(
    page_title="NASA Space Explorer",
    page_icon="🚀",
    layout="wide"
)

# -----------------------
# PLANET DATA
# -----------------------

planet_info = {
    "Mercury": {
        "distance": "57.9 million km",
        "moons": "0",
        "type": "Terrestrial Planet"
    },
    "Venus": {
        "distance": "108.2 million km",
        "moons": "0",
        "type": "Terrestrial Planet"
    },
    "Earth": {
        "distance": "149.6 million km",
        "moons": "1",
        "type": "Terrestrial Planet"
    },
    "Mars": {
        "distance": "227.9 million km",
        "moons": "2",
        "type": "Terrestrial Planet"
    },
    "Jupiter": {
        "distance": "778.5 million km",
        "moons": "95",
        "type": "Gas Giant"
    },
    "Saturn": {
        "distance": "1.4 billion km",
        "moons": "146",
        "type": "Gas Giant"
    },
    "Uranus": {
        "distance": "2.9 billion km",
        "moons": "27",
        "type": "Ice Giant"
    },
    "Neptune": {
        "distance": "4.5 billion km",
        "moons": "14",
        "type": "Ice Giant"
    }
}

# -----------------------
# TITLE
# -----------------------

st.title("🚀 NASA Space Explorer")

st.write(
    "Search for a planet and explore NASA images."
)

# -----------------------
# INPUT
# -----------------------

planet = st.text_input(
    "Enter Planet Name",
    placeholder="Mars"
)

# -----------------------
# SEARCH
# -----------------------

if st.button("Explore Planet"):

    if not planet:
        st.warning("Please enter a planet name.")
        st.stop()

    # NASA IMAGE LIBRARY API
    url = (
        f"https://images-api.nasa.gov/search"
        f"?q={planet}&media_type=image"
    )

    response = requests.get(url)

    data = response.json()

    items = data["collection"]["items"]

    if len(items) == 0:
        st.error("No images found.")
        st.stop()

    st.success(
        f"{len(items)} NASA images found."
    )

    # First Image
    first_item = items[0]

    title = first_item["data"][0].get(
        "title",
        "No Title"
    )

    description = first_item["data"][0].get(
        "description",
        "No Description"
    )

    image_url = first_item["links"][0]["href"]

    st.image(
        image_url,
        caption=title,
        use_container_width=True
    )

    st.subheader("📝 NASA Details")

    st.write(description)

    # Planet Facts
    if planet.title() in planet_info:

        info = planet_info[planet.title()]

        st.subheader("🪐 Planet Facts")

        st.write(
            f"**Type:** {info['type']}"
        )

        st.write(
            f"**Distance from Sun:** {info['distance']}"
        )

        st.write(
            f"**Number of Moons:** {info['moons']}"
        )

    # More Images
    st.subheader("📸 More NASA Images")

    for item in items[:5]:

        try:

            img = item["links"][0]["href"]

            title = item["data"][0]["title"]

            st.image(
                img,
                caption=title,
                width=350
            )

        except:
            pass