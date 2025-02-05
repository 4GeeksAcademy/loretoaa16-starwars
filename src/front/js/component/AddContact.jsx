import React, {useState, useEffect} from "react";

export const AddContact = () => {
    const [contact, setContact] = useState({
        name: "",
        phone: "",
        email: "",
        address: ""
    }
    );
    const [newContact, setNewContact] = useState([]);
    const host = "https://playground.4geeks.com/contact";
    const slug = "loretoaa16";

    const getContacts= async () => {
        const uri = `${host}/agendas/${slug}/contacts`;
       
        const options = {
                method: 'GET' 
            }

        const response = await fetch(uri, options)
        console.log(response)
        if (!response.ok) {
    
            console.log('Error getting contacts', response.status, response.statusText)
            return 
        }

         const data = await response.json()
         console.log("Fetched contacts:", data);
        setNewContact(data.NewContact)
    }  


    useEffect(() => {
      getContacts();
      }, [])

    const handleSubmittNewContact = (event) => {
        event.preventDefault();
        postNewContact();
      }

    const postNewContact = async () => {
        const dataToSend = {
            name: contact.name, // user input for name
            phone: contact.phone, // user input for phone
            email: contact.email, // user input for email
            address: contact.address // user input for address
        };
        const uri = `${host}/agendas/${slug}/contacts`;
        const options = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dataToSend) 
        };
    
        const response = await fetch(uri, options);
        if (!response.ok) {
            console.error('Error posting new contact', response.status, response.statusText);
            return;
        }
    
        const data = await response.json();
        console.log("Contact added:", data);
        getContacts(); 
        setContact({
            name: "",
            phone: "",
            email: "",
            address: ""
        });
    };


    return (
        <form className="container" onSubmit={handleSubmittNewContact}>
            <div className="mb-3">
                <label htmlFor="FullName" className="form-label">Full Name</label>
                <input type="text" className="form-control" id="exampleFullName" name="name" value={contact.name} onChange={(event) => setContact(event.target.value)} placeholder="Full Name" required/>
            </div>
            <div className="mb-3">
                <label htmlFor="exampleInputEmail1" className="form-label">Email address</label>
                <input type="email" className="form-control" id="exampleInputEmail" name="email" value={contact.email} onChange={(event) => setContact(event.target.value)} placeholder="Enter email" required/>
            </div>
            <div className="mb-3">
                <label htmlFor="phoneInput" className="form-label">Phone</label>
                <input type="text" className="form-control" id="exampleInputPhone" name="phone" value={contact.phone} onChange={(event) => setContact(event.target.value)} placeholder="Enter phone" required/>
            </div>
            <div className="mb-3">
                <label htmlFor="AddressInput" className="form-label">Address</label>
                <input type="text" className="form-control" id="exampleInputAddress" name="address" value={contact.address} onChange={(event) => setContact(event.target.value)} placeholder="Enter address" required/>
            </div>
            <button type="submit" className="btn btn-primary">Save</button>
         </form>
    );
}