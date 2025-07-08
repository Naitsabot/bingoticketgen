import io
from typing import List

from ticketgen import ticket_generator, transpose

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Spacer, PageBreak, Table, TableStyle


def create_ticket_element() -> Table:
    """
    Create a single bingo ticket element
    """
    # Generate the ticket data
    data: List[List[str]] = ticket_generator()
    data: List[List[str]] = transpose(data)
    
    # Create a table style for the ticket
    my_table_style: TableStyle = TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 2, colors.black),
        ('BOX', (0, 0), (-1, -1), 5, colors.black),
        ("ROUNDEDCORNERS", (10, 10, 10, 10)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("FONTNAME", (0, 0), (-1, -1), "Courier-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 32),
        ("LEADING", (0, 0), (-1, -1), 42) # give nok rum til fontsize
    ])
    
    # Create the table
    table: Table = Table(data, colWidths=2*cm, rowHeights=2*cm)
    table.setStyle(my_table_style)
    
    # Apply special style to cells containing "69" hehe
    for row_idx, row in enumerate(data):
        for col_idx, cell in enumerate(row):
            if cell == "69":
                special_style: TableStyle = TableStyle([
                    ("FONTNAME", (col_idx, row_idx), (col_idx, row_idx), "Times-Italic")
                ])
                table.setStyle(special_style)
    return table


def PDF_ticket_generator(number_of_tickets: int) -> io.BytesIO:
    """
    Generate a PDF with number_of_tickets bingo tickets
    """
    # Create a buffer to store the PDF
    buffer: io.BytesIO = io.BytesIO()
    
    # Create a list of tickets
    document: List = []
    
    # Create the tickets
    for i in range(number_of_tickets):
        table: Table = create_ticket_element()
        document.append(table)
        
        # Add a page break after every 3 tickets
        if i % 4 == 3:
            document.append(PageBreak())
        else: 
            document.append(Spacer(1, 1*cm))
    
    # Build the PDF
    SimpleDocTemplate(buffer, 
                      pagesize=A4,
                      topMargin=1*cm,
                      bottomMargin=1*cm,
                      leftMargin=1*cm,
                      rightMargin=1*cm).build(document)
    
    # Return the buffer
    buffer.seek(0)
      
    return buffer
