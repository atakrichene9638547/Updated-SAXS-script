
def extract_between(input_str,start,end):
    """ Extract substring from in-between the two input parameters "Start" and "End"

    Args:
        input_str (str): List of the strings 
        start (str): first character to extract
        end (str): last character to extract 

    Returns:
        str: list of extracted strings.
    """
    out_name = []
    for ii in range(len(input_str)):
        start_string = input_str[ii].rfind(str(start))
        last_string = input_str[ii].rfind(str(end))    
        section = input_str[ii][start_string+1:last_string]
        out_name.append(section)
    return out_name