def calculate_bmi(height, weight):
    """
    Calculate Body Mass Index (BMI) given height in meters and weight in kilograms.
    
    BMI = weight (kg) / (height (m))^2
    
    Args:
        height (float): Height in meters
        weight (float): Weight in kilograms
        
    Returns:
        float: BMI value
    """
    if height <= 0 or weight <= 0:
        raise ValueError("Height and weight must be positive values")
        
    bmi = weight / (height ** 2)
    return bmi

def calculate_bmr(height, weight, age, gender):
    """
    Calculate Basal Metabolic Rate (BMR) using the Harris-Benedict equation.
    
    For males:
    BMR = 88.362 + (13.397 × weight in kg) + (4.799 × height in cm) - (5.677 × age in years)
    
    For females:
    BMR = 447.593 + (9.247 × weight in kg) + (3.098 × height in cm) - (4.330 × age in years)
    
    Args:
        height (float): Height in centimeters
        weight (float): Weight in kilograms
        age (float): Age in years
        gender (str): 'male' or 'female'
        
    Returns:
        float: BMR value in calories/day
    """
    if height <= 0 or weight <= 0 or age <= 0:
        raise ValueError("Height, weight, and age must be positive values")
        
    gender = gender.lower()
    
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == 'female':
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")
        
    return bmr