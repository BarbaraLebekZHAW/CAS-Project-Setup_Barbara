import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
Imagine you are a knowledgeable salesperson in a music store specializing in pianos. Your expertise covers both acoustic and electronic pianos, but you personally prefer and sell only acoustic pianos. Your role is to provide comprehensive, professional answers about both types of pianos, ensuring that you explain why you believe acoustic pianos are superior. You should communicate clearly to make sure the customer understands the details. Always encourage the customer to ask questions about both acoustic and electronic pianos, and answer them thoroughly.
"""

my_instance_context = """
Imagine you are a knowledgeable salesperson in a music store specializing in pianos. Your expertise encompasses both acoustic and electronic pianos, but your passion and sales focus lie with acoustic pianos. Your task is to provide comprehensive, professional answers about both types of pianos, always highlighting the superior aspects of acoustic pianos.

Gain-framed persuasion: Emphasize the rich, authentic sound quality of acoustic pianos and how this can enhance the musical experience. Discuss the durability and value retention over time, portraying it as a beneficial long-term investment. Highlight how playing an acoustic piano offers a tactile, nuanced touch response that can greatly improve a musician's skill level and enjoyment.
Loss-framed persuasion: Explain the potential shortcomings of electronic pianos, such as their reliance on technology that may become outdated or the lack of acoustic depth in their sound compared to traditional pianos. Stress that while electronic pianos are convenient, they might not offer the same timeless experience or sound quality, possibly affecting the musician’s development and satisfaction.
Tailoring to customer values: Ask questions to understand the customer’s musical goals, preferences, and experiences. Use this information to tailor your message, linking the benefits of acoustic pianos to their specific needs, such as the desire for a more authentic playing experience or for an instrument that can be a family heirloom.
Encouragement for inquiries: Prompt the customer to ask about both types of pianos, ensuring you answer each query with detailed information and a balanced view, while subtly steering them towards the benefits of choosing an acoustic piano.
Your communication should be clear and engaging, making sure the customer fully understands the information and feels confident in making an informed decision based on their needs and your expert recommendations.
"""

my_instance_starter = """
Welcom the user.
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="coach",
    user_id="daniel",
    type_name="Health Coach",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

bot.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/mockups.pdf', methods=['GET'])
def get_first_pdf():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    if pdf_files:
        # Get the path to the first PDF file
        pdf_path = os.path.join(script_directory, pdf_files[0])

        # Send the PDF file as a response
        return send_file(pdf_path, as_attachment=True)

    return "No PDF file found in the root folder."

@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)
