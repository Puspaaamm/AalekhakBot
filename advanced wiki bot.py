#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Hindi Wikipedia Bot: Infobox and Chart Creator
This bot connects to Hindi Wikipedia and Wikidata to dynamically add/update 
infobox templates and visual data graphs into target articles.
"""

import pywikibot
from pywikibot import pagegenerators

# --- CONFIGURATION SETTINGS ---
# Set DRY_RUN to True to preview edits safely without writing to Wikipedia.
# Set DRY_RUN to False only when you are fully ready to deploy live edits.
DRY_RUN = True  
# ------------------------------

class WikiDataAndChartBot:
    def __init__(self):
        """Initializes connection to Hindi Wikipedia and the global Wikidata repository."""
        self.site = pywikibot.Site('hi', 'wikipedia')
        self.site.login()
        self.repo = self.site.data_repository() # Connects to Wikidata API

    def get_wikidata_claims(self, qid):
        """Fetches all factual statements (claims) for a specific Wikidata Item ID (QID)."""
        try:
            item = pywikibot.ItemPage(self.repo, qid)
            item.get()
            return item.claims
        except Exception as error:
            pywikibot.error(f"Failed to fetch Wikidata for QID {qid}: {error}")
            return None

    def generate_infobox(self, qid, item_type="person"):
        """
        Parses Wikidata properties to generate an accurate Hindi Infobox syntax string.
        Supported item_types: 'person', 'city'
        """
        claims = self.get_wikidata_claims(qid)
        if not claims:
            return ""

        infobox_text = ""

        if item_type == "person":
            # P569 is the Wikidata property ID for Date of Birth
            dob = ""
            if 'P569' in claims:
                dob = claims['P569'][0].getTarget().toTimestr().split('T')[0] # Formats to YYYY-MM-DD

            # P19 is the Wikidata property ID for Place of Birth
            pob = ""
            if 'P19' in claims:
                pob_item = claims['P19'][0].getTarget()
                pob_item.get()
                # Tries to get the Hindi label, falls back to English if missing
                pob = pob_item.labels.get('hi', pob_item.labels.get('en', ''))

            # Assemble the structured template for Hindi Wikipedia
            infobox_text = (
                "{{ज्ञानसंदूक व्यक्ति\n"
                f"| जन्म तिथि = {dob}\n"
                f"| जन्म स्थान = {pob}\n"
                "}}\n"
            )
            
        elif item_type == "city":
            # P1082 is the Wikidata property ID for Population count
            population = ""
            if 'P1082' in claims:
                population = claims['P1082'][0].getTarget().amount

            # Assemble the structured city template for Hindi Wikipedia
            infobox_text = (
                "{{ज्ञानसंदूक शहर\n"
                f"| जनसंख्या = {population}\n"
                "}}\n"
            )

        return infobox_text

    def generate_chart(self, title, x_labels, y_values, chart_type="bar"):
        """
        Generates standard Wikipedia Graph:Chart syntax for visual analytics.
        Supported chart_types: 'bar', 'line', 'pie'
        """
        # Convert lists of labels/values into comma-separated strings required by the template
        x_str = ",".join(map(str, x_labels))
        y_str = ",".join(map(str, y_values))
        
        chart_text = (
            f"{{{{Graph:Chart\n"
            f"| width = 450\n"
            f"| height = 250\n"
            f"| type = {chart_type}\n"
            f"| x = {x_str}\n"
            f"| y = {y_str}\n"
            f"| legend = {title}\n"
            f"}}}}\n"
        )
        return chart_text

    def process_article_update(self, page_title, qid, item_type="person", chart_data=None):
        """Processes the wiki page, inserts missing infoboxes and visual charts, and saves."""
        page = pywikibot.Page(self.site, page_title)
        
        # Skip if the target page is a redirect or does not exist
        if page.isRedirectPage() or not page.exists():
            pywikibot.warning(f"Skipping [[{page_title}]]: Page does not exist or is a redirect.")
            return

        current_text = page.text
        injected_content = ""

        # 1. Generate Infobox if it doesn't already exist in the article text
        if "ज्ञानसंदूक" not in current_text:
            infobox_markup = self.generate_infobox(qid, item_type)
            if infobox_markup:
                injected_content += infobox_markup + "\n"

        # 2. Generate Chart if analytical data is supplied and no chart exists yet
        if chart_data and "Graph:Chart" not in current_text:
            chart_markup = self.generate_chart(
                title=chart_data['title'],
                x_labels=chart_data['x'],
                y_values=chart_data['y'],
                chart_type=chart_data.get('type', 'bar')
            )
            injected_content += chart_markup + "\n"

        # 3. Commit the changes if new elements were successfully structured
        if injected_content:
            # New components are injected right at the top of the article page text
            updated_text = injected_content + current_text
            
            if DRY_RUN:
                pywikibot.output(f"--- [DRY RUN PREVIEW FOR [[{page_title}]]]---")
                pywikibot.output(updated_text[:1200]) # Prints first 1200 characters to console
            else:
                page.text = updated_text
                page.save(
                    summary="बॉट: ज्ञानसंदूक और डेटा चार्ट जोड़ा जा रहा है (विकिडेटा सिंक)",
                    minor=False,
                    botflag=True
                )
                pywikibot.output(f"✅ Successfully updated [[{page_title}]]!")
        else:
            pywikibot.output(f"ℹ️ No new updates required for [[{page_title}]].")

def main():
    """Main entry point to execute the bot operations."""
    bot = WikiDataAndChartBot()
    
    # -------------------------------------------------------------
    # CONFIGURING SAMPLE RUN DATA
    # Target Page: Use your Sandbox first ("सदस्य:YourUsername/प्रयोगपृष्ठ")
    # QID reference: Q9470 (Wikidata QID for Sachin Tendulkar)
    # -------------------------------------------------------------
    target_page = "सदस्य:YourUsername/प्रयोगपृष्ठ"  
    wikidata_qid = "Q9470"  
    
    # Sample analytics data structure for constructing the chart
    sample_chart_data = {
        "title": "Year-wise Performance Analytics",
        "x": ["2022", "2023", "2024", "2025"],
        "y": [1100, 1430, 950, 1200],
        "type": "bar" # Options: 'bar', 'line', 'pie'
    }

    # Execute the operation pipeline
    bot.process_article_update(
        page_title=target_page,
        qid=wikidata_qid,
        item_type="person",
        chart_data=sample_chart_data
    )

if __name__ == "__main__":
    main()

