import requests
import logging
def summarize_text(text):
    try:
        url = "http://127.0.0.1:1234/v1/completions"  # Update with LLaMA 3.2 endpoint
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "meta-llama-3.1-8b-instruct",
            "prompt": f"Summarize the following text while retaining its context:\n\n{text}",
            "max_tokens": 100,  # Adjust for desired length
            "temperature": 0.7  # Controls creativity
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            summary = response.json()["choices"][0]["text"].strip()
            logging.info("Successfully summarized text.")
            return summary
        else:
            logging.error(
                "Text summarization failed: %s, %s",
                response.status_code,
                response.text
            )
            return None
    except Exception as e:
        logging.error("Error in text summarization: %s", e)
        return None




txt="Notre-Dame de Paris (French: [nɔtʁ(ə) dam də paʁi] ⓘ; meaning 'Our Lady of Paris'), often referred to simply as Notre-Dame,[a] is a medieval Catholic cathedral on the Île de la Cité (an island in the River Seine), in the 4th arrondissement of Paris, France. The cathedral, dedicated in honour of the Virgin Mary (Our Lady), is considered one of the finest examples of French Gothic architecture. Several attributes set it apart from the earlier Romanesque style, including its pioneering use of the rib vault and flying buttress, its enormous and colourful rose windows, and the naturalism and abundance of its sculptural decoration.[6] Notre-Dame is also exceptional for its three pipe organs (one historic) and its immense church bells.[7] Construction of the cathedral began in 1163 under Bishop Maurice de Sully and was largely completed by 1260, though it was modified in succeeding centuries. In the 1790s, during the French Revolution, Notre-Dame suffered extensive desecration; much of its religious imagery was damaged or destroyed. In the 19th century, the cathedral hosted the coronation of Napoleon and the funerals of many of the French Republic's presidents. The 1831 publication of Victor Hugo's novel Notre-Dame de Paris (in English: The Hunchback of Notre-Dame) inspired interest which led to restoration between 1844 and 1864, supervised by Eugène Viollet-le-Duc. On 26 August 1944, the Liberation of Paris from German occupation was celebrated in Notre-Dame with the singing of the Magnificat. Beginning in 1963, the cathedral's façade was cleaned of soot and grime. Another cleaning and restoration project was carried out between 1991 and 2000.[8] A fire in April 2019 caused serious damage; but after five years of reconstruction, the cathedral reopened to the general public with a ceremony and by online reservation on 8 December 2024.[9] The cathedral is a widely recognized symbol of the city of Paris and the French nation. In 1805, it was awarded honorary status as a minor basilica. As the cathedral of the archdiocese of Paris, Notre-Dame contains the cathedra or seat of the archbishop of Paris (currently Laurent Ulrich). In the early 21st century, about 12 million people visited Notre-Dame annually, making it the most visited monument in Paris.[10] Over time, the cathedral has gradually been stripped of many decorations and artworks. However, the cathedral still contains Gothic, Baroque, and 19th-century sculptures, 17th- and early 18th-century altarpieces, and some of the most important relics in Christendom, including the Crown of Thorns, and a sliver and nail from the True Cross. Key dates 4th century – Cathedral of Saint Étienne, dedicated to Saint Stephen, built just west of present cathedral.[11] 1163 – Bishop Maurice de Sully begins construction of new cathedral.[11] 1182 or 1185 – Choir completed, clerestory with two levels: upper level of upright windows with pointed arches, still without tracery, lower level of small rose windows. c. 1200 – Construction of nave, with flying buttresses, completed. c. 1210–1220 – Construction of towers begins. c. 1210–1220 – Two new traverses join towers with nave. West rose window complete in 1220. After 1220 – New flying buttresses added to choir walls, remodeling of the clerestories: pointed arched windows are enlarged downward, replacing the triforia, and get tracery."
print(summarize_text(txt))