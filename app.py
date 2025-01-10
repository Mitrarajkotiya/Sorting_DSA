from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

def insertion_sort_with_steps(arr):
    steps = [arr.copy()]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        steps.append(arr.copy())
    return steps

def merge_sort_with_steps(arr):
    steps = []
    steps.append(arr.copy())
    
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sort(arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = sort(arr[:mid])
        right = sort(arr[mid:])
        
        merged = merge(left, right)
        steps.append(merged.copy())
        return merged

    sort(arr)
    return steps

@app.route('/sort', methods=['POST'])
def sort():
    data = request.json
    numbers = data.get('numbers', [])
    algorithm = data.get('algorithm', 'insertion')
    
    try:
        numbers = [int(x) for x in numbers]
        if algorithm == 'insertion':
            sorting_steps = insertion_sort_with_steps(numbers.copy())
        else:
            sorting_steps = merge_sort_with_steps(numbers.copy())
        
        return jsonify({
            'original': numbers,
            'steps': sorting_steps,
            'algorithm': algorithm
        })
    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter numbers only.'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)