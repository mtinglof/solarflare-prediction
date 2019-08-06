data_list = list(none_obs_0, none_obs_1, none_obs_2, none_obs_3, none_obs_4, none_obs_5, 
                 none_obs_6, none_obs_7, none_obs_8, none_obs_9, none_obs_10, 
                 none_obs_11, none_obs_12, none_obs_13, none_obs_14, none_obs_15, none_obs_16, none_obs_17,
                 none_obs_18, none_obs_19, none_obs_20, none_obs_21, none_obs_22, none_obs_23, none_obs_24, 
                 none_obs_25, none_obs_26, none_obs_27, none_obs_28, none_obs_29)

solar_data_list = list(solar_obs_0, solar_obs_1, solar_obs_2, solar_obs_3, solar_obs_4)

aic_hold = list(0)
hit = 0 

for (data_item in data_list){
  obs = dim(data_item)[1]/60
  index = 0
  min_row = 1 
  max_row = 60 
  
  index_range = sample(seq(0, obs-1), 1000)
  
  for (index in index_range){
    min_row = (index * 60) + 1
    max_row = min_row + 59
    aic = arima(data_item[min_row : max_row, 2], c(0, 1, 0))[['aic']][1]
    if (aic < -9999){
      hit = hit + 1
    } 
    else{
      aic_hold[[1]] = list.append(aic_hold[[1]], aic)
    }
  }
}

max_lim = length(aic_hold[[1]])

hist(aic_hold[[1]][2:max_lim])
mean(aic_hold[[1]][2:max_lim])
sd(aic_hold[[1]][2:max_lim])
print(hit)