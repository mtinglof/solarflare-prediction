def stats(tested_creatures): 
    num_of_genes = 0 
    size_of_input = 0 
    count = 0 
    for species in tested_creatures: 
        num_of_genes += len(species['creatures'][0].getCreature()['genome'])
        size_of_input += species['creatures'][0].getCreature()['input_length']
        count += 1
    num_of_genes = num_of_genes/count
    size_of_input = size_of_input/count
    input_per_gene = size_of_input/num_of_genes
    return([num_of_genes, size_of_input, input_per_gene])