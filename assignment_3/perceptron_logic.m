logic_gate_input = transpose([ 0 0; 0 1; 1 0; 1 1 ]);

logic_gate_output_and = [ 0 0 0 1 ];
logic_gate_output_or  = [ 0 1 1 1 ];
logic_gate_output_xor = [ 0 1 1 0 ];

[x, y] = perceptron_train(logic_gate_input, logic_gate_output_or, 0.1, 0, 500)