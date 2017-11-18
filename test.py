# This file is part of pylabels, a Python library to create PDFs for printing
# labels.
# Copyright (C) 2012, 2013, 2014 Blair Bonnett
#
# pylabels is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pylabels is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pylabels.  If not, see <http://www.gnu.org/licenses/>.

import labels
from reportlab.graphics import shapes

# Create an A4 portrait (210mm x 297mm) sheets with 2 columns and 8 rows of
# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = labels.Specification(
    sheet_width=215.9,
    sheet_height=279.4,
    columns=2,
    rows=5,
    label_width=101.6,
    label_height=50.8,
    left_margin=6.2,
    column_gap=4.8,
    row_gap=0,
)
# Create a function to draw each label. This will be given the ReportLab drawing
# object to draw on, the dimensions (NB. these will be in points, the unit
# ReportLab uses) of the label, and the object to render.
def draw_label(label, width, height, obj):
    # Just convert the object to a string and print this at the bottom left of
    # the label.
    label.add(shapes.String(width/2.0, height/2.0, str(obj), fontName="Helvetica", fontSize=40, textAnchor = 'middle'))

# Create the sheet.
sheet = labels.Sheet(specs, draw_label, border=False)

# We can also add each item from an iterable.
sheet.add_labels(range(1, 10))

# Note that any oversize label is automatically trimmed to prevent it messing up
# other labels.

# Save the file and we are done.
sheet.save('basic.pdf')
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))
