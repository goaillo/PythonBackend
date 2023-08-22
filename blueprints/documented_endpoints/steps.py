from flask import Blueprint
blueprint = Blueprint('step', __name__)

def serialize_step(step_id):
    return {
        "step_id": step_id,
        "step": 'step'
    }

@blueprint.get('/step/<int:step_id>')
def return_step(step_id):
    # show the step with the given id, the id is an integer
    return serialize_step(step_id)


@blueprint.post('/step')
def create_step():
    # show the step with the given id, the id is an integer
    # TODO Create a real step
    return serialize_step(step_id=1)