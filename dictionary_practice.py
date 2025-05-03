import streamlit as st
import numpy as np

st.title("Split That")
st.markdown("<i>An easy way to split costs between friends</i>", unsafe_allow_html=True)
st.markdown("Please input the names of group members below, separated by <span style='color:indianred'>commas</span> :", unsafe_allow_html=True)
raw_user_input = st.text_input(" ")

if raw_user_input:
    names_list = [name.strip() for name in raw_user_input.split(",") if name.strip()]
    #st.write("People in the group:", names_list)
    # uncomment above to see the list of names
    
    Payments_dictionary = {name: [] for name in names_list}
    numpeeps = len(Payments_dictionary) #number of group members
    vector_with_avgs = [] #this is the list of totals of what one person paid/group size

    for i in names_list: #individual_payments is the list of payments for one name
        st.markdown("<br>", unsafe_allow_html=True)
        individual_payments = st.text_input(f"Enter {i}'s payments (one or more), separated by commas :") #i is eah name in this case
        
        if individual_payments:
            clean_payments = []
            for p in individual_payments.split(","):
                p = p.strip()
                if not p:
                    continue
                try:
                    clean_payments.append(float(p))
                except ValueError:
                    st.warning(f"⚠️ Invalid entry, Please delete: '{p}'")

            Payments_dictionary[i] = clean_payments
            vector_with_avgs.append(sum(clean_payments) / numpeeps)
   
    if len(vector_with_avgs) == numpeeps:
        Everyone_pays = (sum(vector_with_avgs))
        owes_matrix = np.zeros((numpeeps,numpeeps))
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"Everyone should expect to contribute: <span style='color:lightgreen;'>${Everyone_pays:.2f}</span>", unsafe_allow_html=True)

        #filling the owes_matrix
        for i_index in range(len(owes_matrix)):
            owes_matrix[i_index,:] = vector_with_avgs[i_index] 
            owes_matrix[i_index,i_index] = 0 

        # checkbox toggle for simplifying payments
        show_simplified = st.checkbox("Show simplified (net) payments", help="Only show net owed amounts between people"):
        if show_simplified:
            st.markdown("<hr><h3>Simplified Payments</h3>", unsafe_allow_html=True)
            
            for j in range(len(owes_matrix)):
                st.markdown(f"<h4 style='margin-top: 2em'>{names_list[j]} Pays</h4>", unsafe_allow_html=True)
                payment = False
                
                for i in range(len(individual_vector)):
                    if i != j:
                        net_payment = owes_matrix[i, j] - owes_matrix[j, i]
                        if net_payment > 0:
                            st.write(f"<span style='color:lightgreen;'>${net_payment:.2f}</span> to <b>{names_list[i]}</b>", unsafe_allow_html=True)
                            payment = True
        
                if not payment:
                    st.write("Pays nothing")

        else:
        #printing out final numbers
            for j in range(len(owes_matrix)):
                individual_vector = owes_matrix[j,:]
                #the list () below makes the dictionary a list with the keys being able to be indexes now
                st.markdown(f"<h4 style='margin-top: 2em'>{list(Payments_dictionary.keys())[j]} Pays</h4>", unsafe_allow_html=True)
                for i in range(len(individual_vector)):
                    if j != i: #skipping outputting the "sara pays sara $0" if sara has a 0 vector
                        st.write(f"<span style='color:lightgreen;'>${owes_matrix[i,j]:.2f}</span> to <b>{list(Payments_dictionary.keys())[i]}</b>",unsafe_allow_html=True)
    
