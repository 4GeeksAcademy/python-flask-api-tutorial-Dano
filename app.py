from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista inicial como diccionarios con id
todos = [
    {"id": 1, "todo": "cocinar"},
    {"id": 2, "todo": "comer"},
    {"id": 3, "todo": "recoger"},
    {"id": 4, "todo": "limpiar"}
]

# GET → obtener todos los ToDos
@app.route('/todos', methods=['GET'])
def get_todos():
    if not todos:
        return jsonify({"msg": "No hay ToDos disponibles"}), 200
    return jsonify({"data": todos}), 200

# POST → agregar un nuevo ToDo
@app.route('/todos', methods=['POST'])
def add_todo():
    body = request.get_json()  # sin silent=True
    if body is None or 'todo' not in body:
        return jsonify({"msg": "El campo 'todo' es obligatorio"}), 400

    new_todo = {
        "id": len(todos) + 1,     # ojo: si borras, los ids pueden reutilizarse
        "todo": body['todo']
    }
    todos.append(new_todo)

    print(body)
    return jsonify({"msg": "ToDo agregado exitosamente!", "data": new_todo}), 200

# DELETE → eliminar un ToDo por id
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        return jsonify({"msg": "No se encontró el ToDo con id {}".format(todo_id)}), 404

    todos = [todo for todo in todos if todo["id"] != todo_id]
    print("Eliminando ToDo con id: {}".format(todo_id))
    return jsonify({"msg": "ToDo con id {} eliminado correctamente".format(todo_id)}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)