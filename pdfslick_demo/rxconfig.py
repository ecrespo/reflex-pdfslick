import reflex as rx

config = rx.Config(
    app_name="pdfslick_demo",
    plugins=[
        # The demo uses Radix Themes components; enable the stylesheet
        # explicitly (implicit enablement is deprecated in Reflex 0.9+).
        rx.plugins.RadixThemesPlugin(),
        rx.plugins.SitemapPlugin(),
    ],
)
