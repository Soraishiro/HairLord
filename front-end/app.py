import streamlit as st
import pandas as pd
from io import StringIO
from pathlib import Path

# Init model
from hair_swap import HairFast,get_parser
# import requests
from io import BytesIO
from PIL import Image
# from functools import cache

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import torchvision.transforms as T
import torch


if "model" not in st.session_state.keys():
    model_args = get_parser()
    hair_fast = HairFast(model_args.parse_args([]))
    st.session_state["model"] = hair_fast

hair_fast = st.session_state["model"]

st.set_page_config(
        page_title="Virtual Hair",
)

st.title("Salon ABC - Virtual Hair Style")
input_face = st.file_uploader("Chọn ảnh khuôn mặt bạn")
hair_shape = st.file_uploader("Chọn ảnh mẫu tóc")
hair_color = st.file_uploader("Chọn ảnh màu tóc")


if st.button("Change me!!!", type="primary"):
    # st.image('result.png', caption='Sunrise by the mountains')

    if input_face is not None and hair_shape is not None and hair_color is not None:
        # To read file as bytes:
        save_folder = '/content/HairFastGAN/upload'
        face_path = Path(save_folder, input_face.name)
        with open(face_path, mode='wb') as w:
            w.write(input_face.getvalue())
        shape_path = Path(save_folder, hair_shape.name)
        with open(shape_path, mode='wb') as w:
            w.write(hair_shape.getvalue())
        color_path = Path(save_folder, hair_color.name)
        with open(color_path, mode='wb') as w:
            w.write(hair_color.getvalue())

        final_image, face_align, shape_align, color_align =  hair_fast.swap(face_path, shape_path, color_path, align=True)
        # Save output to file ressult.png
        save_path = Path(save_folder, 'result.png')
        final_image = T.functional.to_pil_image(final_image)
        # final_image.save(save_path)
        st.image(final_image, caption='Render result')
        del final_image, face_align, shape_align, color_align
