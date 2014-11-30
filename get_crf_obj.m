function [obj,g_w,g_t] = get_crf_obj(A, W, T, c)
    
    [~,n] = size(A);
    label = A(2,:)-96;
    next_id = A(3,:);
    pixel = A(6:133,:);    
    
    g_w = zeros(128,26);
    g_t = zeros(26,26);
    obj = 0;
    
    start_id = 1;
    w_ctr = 0;
    for w_idx=1:n
        if next_id(w_idx)==-1
            
            end_id = w_idx;
            len = end_id-start_id+1;
            w_pix = pixel(:,start_id:end_id);
            w_label = label(:,start_id:end_id);
            
            % log of Z
            [forward,backward,log_z] = log_z_obj(w_pix,len,W,T);
            % marginal probabilities
            [w_marginal,t_marginal] = marginal(w_pix,len,W,T,forward,backward,log_z);
%             fun = @(W)log_p(w_pix,w_label,len,W,T,log_z);
%             [grad,err,finaldelta] = gradest(fun,W);
            % log gradient
            [tg_w,tg_t] = log_grad(w_pix,w_label,len,w_marginal,t_marginal);
            
            obj = obj + log_p(w_pix,w_label,len,W,T,log_z);
            g_w = g_w+tg_w;
            g_t = g_t+tg_t;
            start_id = end_id+1;
            w_ctr = w_ctr+1;
        end
    end
    grad = [g_w(:); g_t(:)]/w_ctr;
    % objective function
    obj = -c*obj/w_ctr + term2(W) + term3(T);
    % gradient of objective function
    g_w = -c*g_w/w_ctr+W;
    g_t = -c*g_t/w_ctr+T;
    
end

% 2nd term of objective function
function val = term2(W)
    val = 0;
    for i=1:26
        val = val + norm(W(:,i))^2;
    end
    val = 0.5*val;
end

% 3rd term of objective function
function val = term3(T)
    val = 0.5*sum(sum(T.*T));
end

% marginal probabilities
function [w_marginal,t_marginal] = marginal(X,len,W,T,forward,backward,log_z)
    w_marginal = forward.*backward./exp(W'*X)/exp(log_z);
    t_marginal = zeros(len-1,26,26);
    for z=1:len-1
        t_marginal(z,:,:) = forward(:,z)*backward(:,z+1)'.*exp(T)/exp(log_z);
    end
end

% gradient of log p(y|x)
function [g_w,g_t] = log_grad(pixel,label,len,w_marginal,t_marginal)
    g_w = -pixel*w_marginal';
    for z=1:len
        i = label(z);
        g_w(:,i) = g_w(:,i) + pixel(:,z);
    end
    
    g_t = reshape(-sum(t_marginal),[26,26]);
    for z=1:len-1
        i = label(z);
        j = label(z+1);
        g_t(i,j) = g_t(i,j)+1;
    end
end

% log p(y|x)
function val = log_p(pixel,label,len,W,T,log_z)
    val = sum(sum(pixel.*W(:,label)));
    for z=1:len-1
        val = val + T(label(z),label(z+1));
    end
    val = val-log_z;
end

% log of Z
function [forward,backward,val] = log_z_obj(X,len,W,T)
    forward = zeros(26,len);
    forward(:,1) = exp(term_1(X(:,1),W));    
    for j = 2:len
        forward(:,j) = forward(:,j-1)'*exp(T);
        forward(:,j) = forward(:,j).*exp(term_1(X(:,j),W));
    end
    
    backward = zeros(26,len);
    backward(:,1) = exp(term_1(X(:,len),W));

    for j = 2:len
        backward(:,j) = backward(:,j-1)'*exp(T');
        backward(:,j) = backward(:,j).*exp(term_1(X(:,len-j+1),W));
    end
    val = log(sum(backward(:,len)));
    backward = fliplr(backward);
end

% only used in log_z_obj
function prod = term_1(x,W)
    prod = (x'*W)';
end
