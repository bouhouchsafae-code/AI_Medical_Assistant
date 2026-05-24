from reportlab.platypus import (

    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle

)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib import colors

from reportlab.lib.pagesizes import letter

from reportlab.platypus.flowables import HRFlowable

# =========================
# 📄 GENERATE PDF
# =========================

def generate_pdf(

    report_text,

    filename="medical_report.pdf"

):

    # =========================
    # 📄 DOCUMENT
    # =========================

    doc = SimpleDocTemplate(

        filename,

        pagesize=letter,

        rightMargin=40,

        leftMargin=40,

        topMargin=40,

        bottomMargin=30

    )

    # =========================
    # 🎨 STYLES
    # =========================

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]

    normal_style = styles["BodyText"]

    title_style.textColor = colors.HexColor(
        "#1565C0"
    )

    normal_style.textColor = colors.black

    normal_style.leading = 22

    # =========================
    # 📦 CONTENT
    # =========================

    content = []

    # =========================
    # 🏥 HEADER
    # =========================

    content.append(

        Paragraph(

            "AI Medical Diagnostic Report",

            title_style

        )

    )

    content.append(
        Spacer(1, 15)
    )

    content.append(

        HRFlowable(

            width="100%",

            color=colors.grey

        )

    )

    content.append(
        Spacer(1, 20)
    )

    # =========================
    # 📜 REPORT LINES
    # =========================

    lines = report_text.split("\n")

    for line in lines:

        clean_line = line.strip()

        if clean_line != "":

            # =========================
            # 🔵 SECTION TITLES
            # =========================

            if ":" in clean_line:

                parts = clean_line.split(
                    ":",
                    1
                )

                key = parts[0]

                value = parts[1]

                table_data = [

                    [

                        Paragraph(

                            f"<b>{key}</b>",

                            normal_style

                        ),

                        Paragraph(

                            value,

                            normal_style

                        )

                    ]

                ]

                table = Table(

                    table_data,

                    colWidths=[160, 320]

                )

                table.setStyle(

                    TableStyle([

                        (

                            "BACKGROUND",

                            (0, 0),

                            (0, 0),

                            colors.HexColor(
                                "#E3F2FD"
                            )

                        ),

                        (

                            "TEXTCOLOR",

                            (0, 0),

                            (-1, -1),

                            colors.black

                        ),

                        (

                            "GRID",

                            (0, 0),

                            (-1, -1),

                            1,

                            colors.lightgrey

                        ),

                        (

                            "FONTNAME",

                            (0, 0),

                            (0, 0),

                            "Helvetica-Bold"

                        ),

                        (

                            "BOTTOMPADDING",

                            (0, 0),

                            (-1, -1),

                            10

                        ),

                        (

                            "TOPPADDING",

                            (0, 0),

                            (-1, -1),

                            10

                        )

                    ])

                )

                content.append(table)

                content.append(
                    Spacer(1, 12)
                )

            # =========================
            # 📄 NORMAL TEXT
            # =========================

            else:

                content.append(

                    Paragraph(

                        clean_line,

                        normal_style

                    )

                )

                content.append(
                    Spacer(1, 10)
                )

    # =========================
    # ⚠️ FOOTER
    # =========================

    content.append(
        Spacer(1, 25)
    )

    content.append(

        HRFlowable(

            width="100%",

            color=colors.grey

        )

    )

    content.append(
        Spacer(1, 12)
    )

    content.append(

        Paragraph(

            "<font color='red'><b>Disclaimer:</b></font> "
            "This AI-generated report is intended "
            "for medical assistance only and does "
            "not replace professional clinical diagnosis.",

            normal_style

        )

    )

    # =========================
    # 🚀 BUILD PDF
    # =========================

    doc.build(content)

    return filename