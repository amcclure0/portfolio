import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode
import pandas as pd

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "link": [
        "https://www.gstatic.com/flights/airline_logos/70px/ET.png",
        "https://i.imgur.com/bvHZX5j.png",
        "https://i.imgur.com/D7xDwT9.png",
    ],
}

df = pd.DataFrame(data)
gb = GridOptionsBuilder.from_dataframe(df,
                                        editable=True)

thumbnail_renderer = JsCode("""
    class ThumbnailRenderer {
        init(params) {

        this.eGui = document.createElement('img');
        this.eGui.setAttribute('src', params.value);
        this.eGui.setAttribute('width', '40');
        this.eGui.setAttribute('height', '40');
        }
            getGui() {
            console.log(this.eGui);

            return this.eGui;
        }
    }
""")

gb.configure_column('link', cellRenderer=thumbnail_renderer)

grid = AgGrid(df,
            gridOptions=gb.build(),
            updateMode=GridUpdateMode.VALUE_CHANGED,
            allow_unsafe_jscode=True)
