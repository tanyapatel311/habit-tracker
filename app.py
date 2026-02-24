from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary List that will be replaced with MongoDB soon
todos = []

@app.route("/")
def index():
      return render_template("index.html", todos=todos)

@app.route("/new")
def new():
      return render_template("new.html")

@app.route("/add", methods = ["POST"])
def add():
      title = request.form.get("title", "").strip()
      if title:
            todos.append({"title": title, "done": False})
      return redirect(url_for("index"))

if __name__ == "__main__":
      app.run(host="0.0.0.0", port=8080, debug=True)
      