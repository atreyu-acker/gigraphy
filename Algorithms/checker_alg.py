

def check_coefficients(user_inputs, correct_coefficients, tolerance=0.1):
    
    results = {}
    all_correct = True

    for key, correct_val in correct_coefficients.items():
        
        try:
            user_val = float(user_inputs.get(key, ""))
        except (ValueError, TypeError):
            results[key] = "invalid"
            all_correct = False
            continue

        if abs(user_val - correct_val) <= tolerance:
            results[key] = "correct"
        else:
            results[key] = "incorrect"
            all_correct = False

    return all_correct, results