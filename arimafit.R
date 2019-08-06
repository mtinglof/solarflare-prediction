arma_list = list() 
count_list = list()
found = FALSE

data_list = list(none_obs_0, none_obs_1, none_obs_2, none_obs_3, none_obs_4, none_obs_5, 
                 none_obs_6, none_obs_7, none_obs_8, none_obs_9, none_obs_10, 
                 none_obs_11, none_obs_12, none_obs_13, none_obs_14, none_obs_15, none_obs_16, none_obs_17,
                 none_obs_18, none_obs_19, none_obs_20, none_obs_21, none_obs_22, none_obs_23, none_obs_24, 
                 none_obs_25, none_obs_26, none_obs_27, none_obs_28, none_obs_29)

item_count = 1

for (data_item in data_list){
  obs = dim(data_item)[1]/60
  index = 0
  min_row = 1 
  max_row = 60 
  
  index_range = sample(seq(0, obs-1), 100)
  
  for (index in index_range){
    min_row = (index * 60) + 1
    max_row = min_row + 59
    data_full = data_item[min_row : max_row, 26]
    data_transformed = (data_full - median(data_full))/sd(data_full)
    data_arima_order = arimaorder(auto.arima(ts(data_transformed)))
    
    count_index = 1
    for (order in arma_list){
      if(identical(data_arima_order, order)){
        count_list[count_index] = count_list[[count_index]][1] + 1 
        found = TRUE
      }
      count_index = count_index + 1
    }
    if (found){
      found = FALSE
    }
    else{
      arma_list = list.append(arma_list, data_arima_order)
      count_list = list.append(count_list, 1)
    }
    index = index + 1
  }
  if (item_count%%5 == 0){
    print(item_count)
  }
  item_count = item_count + 1
}

View(arma_list)
View(count_list)