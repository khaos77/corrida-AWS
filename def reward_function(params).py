def reward_function(params):
    # Input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']  # Use speed directly (avoid referencing max_speed)
    progress = params['progress']
    steps = params['steps']
    all_wheels_on_track = params['all_wheels_on_track']
    is_reversed = params['is_reversed']
    
    # Initialize reward
    reward = 1e-3  # Small base reward
    
    # 1. Speed Optimization (use normalized speed instead of max_speed)
    # Assuming max_speed is ~4.0 (typical for DeepRacer), normalize speed between 0-1
    normalized_speed = speed / 4.0  # Replace 4.0 with your expected max speed
    speed_reward = normalized_speed ** 3  # Cubic incentive for higher speeds
    reward += speed_reward * 3.0
    
    # 2. Optimal Racing Line (15% offset from center)
    optimal_offset = 0.15 * track_width
    distance_penalty = abs(distance_from_center - optimal_offset) / track_width
    reward += (1 - distance_penalty) * 2.0
    
    # 3. Progress Incentive (encourage faster laps)
    reward += (progress / steps) * 4.0
    
    # 4. Penalties
    if not all_wheels_on_track:
        reward *= 0.2  # Harsh penalty for going off-track
    elif speed < 0.5 * 4.0:  # Replace 4.0 with expected max speed
        reward *= 0.5  # Penalize slow speeds
    
    return float(max(reward, 1e-3))  # Ensure non-zero reward