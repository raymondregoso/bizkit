from flask import Blueprint, request, jsonify

from .data.search_data import USERS  

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    args = request.args.to_dict()
    results = search_users(args)
    return jsonify(results), 200

def search_users(args):
    """Search users database based on specified search parameters

    Parameters:
        args: a dictionary containing the search parameters from request args

    Returns:
        a list of users that match the search parameters, ensuring each user is included only once
    """
    results = []
    seen_ids = set()

    for user in USERS:
        if 'id' in args and user['id'] == args['id'] and user['id'] not in seen_ids:
            results.append(user)
            seen_ids.add(user['id'])
            continue

        if 'name' in args and args['name'].lower() in user['name'].lower() and user['id'] not in seen_ids:
            results.append(user)
            seen_ids.add(user['id'])
            continue

        if 'age' in args:
            user_age = user.get('age', 0)  
            search_age = int(args['age'])
            if user_age >= search_age - 1 and user_age <= search_age + 1 and user['id'] not in seen_ids:
                results.append(user)
                seen_ids.add(user['id'])
                continue

        if 'occupation' in args and args['occupation'].lower() in user['occupation'].lower() and user['id'] not in seen_ids:
            results.append(user)
            seen_ids.add(user['id'])
            continue

        if not any(args.values()) and user['id'] not in seen_ids:  # No search parameters provided
            results.append(user)
            seen_ids.add(user['id'])

    return results
