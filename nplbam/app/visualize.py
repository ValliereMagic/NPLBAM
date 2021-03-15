from flask import Blueprint, redirect, render_template, request, Response
from flask import session as flask_session
from sqlalchemy.orm import Query, relationship, sessionmaker

from .db import db

import io
import numpy as np

from datetime import date

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


bp = Blueprint('visualize', __name__, url_prefix="")

@bp.route("/visualize")
def visualize():
    # Make sure the user is userLVL 0 or 1
    user_level: int = flask_session.get("userLVL", default=None)
    # Rely on short circuit eval here...
    if (user_level is None) or user_level > 1:
        # May need to change where we redirect them in the future
        return redirect("/")
    return render_template("visualize.html", title="Visualize")



@bp.route("/visual_durations.png")
def visual_image1_png():
    """ 
    This is a image that is dynamically generated by plots from the database.
    This image is a 3x3 subplot of Durations in each stage and overall.
    """
    # Open a database session
    engine = db.get_db_engine()
    db_session = (sessionmaker(bind=engine))()
    
    # Pull the last 6 months of data
    data_list = db_session.query(db.MetaInformation).\
        order_by(db.MetaInformation.year.desc(), db.MetaInformation.month.desc()).\
        limit(6).all()
    
    # Close the database like a good boy
    db_session.close()

    # Get the length of our list
    x = len(data_list)    

    # create empty arrays to hold our values for visualization
    months = np.empty(x, dtype=object)
    stage1 = np.empty(x, dtype=float)
    stage2 = np.empty(x, dtype=float)    
    stage3 = np.empty(x, dtype=float)    
    stage4 = np.empty(x, dtype=float)    
    stage5 = np.empty(x, dtype=float)    
    stage6 = np.empty(x, dtype=float)    
    stage7 = np.empty(x, dtype=float) 
    total = np.empty(x, dtype=float)   

    # Go row by row in our list taken from the database and put them in the arrays
    for row in data_list:
        # We want to put them into the array in reverse. (Using our amount pulled from database)
        # so that the most recent month is to the right of the visualization
        x -= 1
        # Month as an number with 1 leading 0
        months[x] = "{:02d}".format(row.month)
        # Figure out the average by taking total amount / #of animals
        stage1[x] = (row.totalDaysCompStage1/row.animalsCompStage1)
        stage2[x] = (row.totalDaysCompStage2/row.animalsCompStage2)
        stage3[x] = (row.totalDaysCompStage3/row.animalsCompStage3)
        stage4[x] = (row.totalDaysCompStage4/row.animalsCompStage4)
        stage5[x] = (row.totalDaysCompStage5/row.animalsCompStage5)
        stage6[x] = (row.totalDaysCompStage6/row.animalsCompStage6)
        stage7[x] = (row.totalDaysCompStage7/row.animalsCompStage7)
        total[x] = (row.totalStagesLength/row.totalStagesAmount)

    # Create a subplot matrix (3x3)
    fig, axs = plt.subplots(3, 3)
    # Add a Title
    fig.suptitle("Average Duration in Stages", fontsize='xx-large')
    # Add a y label
    fig.text(0.5, 0.04, 'Month', ha='center', va='center', fontsize='large')
    # Add a x label
    fig.text(0.06, 0.5, 'Average Duration (Days)', ha='center', va='center', rotation='vertical', fontsize='large')
    # Add a note at the bottom left for the date
    fig.text(0, 0, 'Created on {}'.format(date.today()))
    # Set axis plots with our data
    # Stage 1
    axs[0, 0].plot(months, stage1, 'b')
    axs[0, 0].set_title(label="Stage 1", y=1)
    # Stage 2
    axs[0, 1].plot(months, stage2, 'b')
    axs[0, 1].set_title(label="Stage 2", y=1)
    # Stage 3
    axs[0, 2].plot(months, stage3, 'b')
    axs[0, 2].set_title(label="Stage 3", y=1)
    # Stage 4
    axs[1, 0].plot(months, stage4, 'b')
    axs[1, 0].set_title(label="Stage 4", y=1)
    # Stage 5
    axs[1, 1].plot(months, stage5, 'b')
    axs[1, 1].set_title(label="Stage 5", y=1)
    # Stage 6
    axs[1, 2].plot(months, stage6, 'b')
    axs[1, 2].set_title(label="Stage 6", y=1)
    # Stage 7
    axs[2, 0].plot(months, stage7, 'b')
    axs[2, 0].set_title(label="Stage 7", y=1)
    # Stage Total
    axs[2, 1].plot(months, total, 'm')
    axs[2, 1].set_title(label="Full Length", y=1)
    # Unused Axis, so just hide
    axs[2, 2].set_axis_off()

    # Adjust the margins between subplots
    plt.subplots_adjust(wspace=0.25, hspace=1)

    # Go through each axis and set the base to 0
    for ax in axs.flat:
        ax.set_ylim(ymin=0)

    # Convert the graph to a png
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close
    # Return the png
    return Response(output.getvalue(), mimetype='image/png')
