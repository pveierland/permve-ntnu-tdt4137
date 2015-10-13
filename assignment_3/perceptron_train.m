function [ weights, epochs ] = perceptron_train( training_set_inputs, training_set_outputs, alpha, theta, max_epochs )

[p_rows, p_cols] = size(training_set_inputs);
weights = rand(1, p_rows);

for epoch = 1:max_epochs
    epochs      = epoch;
    error_found = 0;
    
    for i = 1:p_cols
        output = hardlim(weights * training_set_inputs(:,i) - theta + 0.000001);
        error  = training_set_outputs(i) - output;
        
        if error ~= 0
            error_found = 1;
        end
        
        fprintf('%d & %.0f & %.0f & %.0f & %.3f & %.3f & %.0f & %.0f & ', ...
            epoch, ...
            training_set_inputs(1,i), ...
            training_set_inputs(2,i), ...
            training_set_outputs(i), ...
            weights(1,1), ...
            weights(1,2), ...
            output, ...
            error)

        % Update weights
        dw = alpha * training_set_inputs(:,i) * error;
        weights  = weights + transpose(dw);
        
        fprintf('%.3f & %.3f \\\\\n', ...
            weights(1,1), ...
            weights(1,2))
    end
    
    if error_found == 0
        break
    end
end

end