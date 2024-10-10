###album catalog: cold-storage

import os
from album.runner.api import setup, get_data_path
    

def run():
    import napari
    from blik.widgets.main_widget import MainBlikWidget

    viewer = napari.Viewer()

    widget = MainBlikWidget()
    viewer.window.add_dock_widget(widget)

    napari.run()

setup(
    group="brisvag",
    name="blik",
    version="0.0.1",
    title="blik: a Python tool for visualising and interacting with cryo-ET and subtomogram averaging data.",
    description="blik is a Python tool for visualising and interacting with cryo-ET and subtomogram averaging data.",
    solution_creators=["Kyle Harrington"],
    cite=[{"text": "Gaifas, L., Timmins, J. and Gutsche, I., 2023. blik: an extensible napari plugin for cryo-ET data visualisation, annotation and analysis. bioRxiv, pp.2023-12..", "url": "https://brisvag.github.io/blik/"}],
    tags=["imaging", "cryoet", "Python", "napari"],
    license="GPL v3.0",
    covers=[
        {
            "description": "Screenshot of blik.",
            "source": "cover.png",
        }
    ],
    album_api_version="0.5.1",
    args=[
    ],
    run=run,
    dependencies={
        "parent": {
            "group": "napari",
            "name": "napyro",
            "version": "0.0.3",
        }
    },
)
