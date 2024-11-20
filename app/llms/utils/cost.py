_costs = {
    "input_tokens": 0.15,
    "output_tokens": 0.60,
}


def calculate_cost(input_tokens, output_tokens):
    input_cost = (input_tokens / 1e6) * _costs["input_tokens"]
    output_cost = (output_tokens / 1e6) * _costs["output_tokens"]
    total_cost = input_cost + output_cost
    return (total_cost, input_cost, output_cost)
