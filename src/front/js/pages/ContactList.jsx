import React, { useContext, useState, useEffect } from "react";
import {Link} from "react-router-dom";
import { Context } from "../store/appContext.js";
import { useNavigate } from "react-router-dom";

export const ContactList = () => {
    const [name, setName] = useState("");
    const [phone, setPhone] = useState("");
    const [email, setEmail] = useState("");
    const [address,setAddress] = useState("");
    const { store, actions } = useContext(Context);
    const navigate = useNavigate();
    
    const setEditingContact = (item) => {
    setName(item.name)
    setPhone(item.phone)
    setEmail(item.email)
    setAddress(item.address)
    }

    const handleSubmitEdit = (event, id) => {
        event.preventDefault();
        const dataToSend = {name, phone, email, address};
        actions.editContact(id, dataToSend)
        navigate("/contact-List");
    }
    const handleDeleteContact = (id) => {
        actions.deleteContact(id)
        navigate("/contact-list");
    }
    useEffect(() => {
        actions.getContacts();
            
            }, [navigate]);
    
    return (
    <div className="container">
    <h1 className="text-center">Contact List</h1>
 
    <Link to="/Add-Contact"><button type="button" className="btn btn-primary">Add Contact</button></Link>
   
    {store.contacts.map((item) => 
        <div className="card mb-3" key={item.id}>
        <div className="row g-0">
            <div className="col-md-4">
                <img src="https://plus.unsplash.com/premium_photo-1683865775275-a576c7588bc8?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8cGVyZmlsJTIwZGUlMjB1c3VhcmlvfGVufDB8fDB8fHww"
                 className="img-fluid rounded-start w-100 h-100" alt="..." />
            </div>
            <div className="col-md-8">
                <div className="card-body d-grid m-3">
                    <span className="text-end">
                        <i className="fas fa-edit text-secondary me-2" data-bs-toggle="modal" data-bs-target={`#editModal${item.id}`} onClick={() => setEditingContact(item, item.id)}></i>
                        {store.contacts.map((iterator) => 
                                <div className="modal fade" key={iterator.id} id={`editModal${iterator.id}`} tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div className="modal-dialog">
                                    <div className="modal-content">
                                    <div className="modal-header">
                                        <h1 className="modal-title fs-5" id="exampleModalLabel">Edit Contact</h1>
                                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div className="modal-body">
                                        <form className="container" onSubmit={(event) => handleSubmitEdit(event, iterator.id)}>
                                            <div className="mb-3">
                                                <label htmlFor="FullName" className="form-label">Full Name</label>
                                                <input type="text" className="form-control" id="exampleFullName" name="name" value={name} onChange={(event) => setName(event.target.value)} placeholder={iterator.name} required />
                                            </div>
                                            <div className="mb-3">
                                                <label htmlFor="exampleInputEmail1" className="form-label">Email address</label>
                                                <input type="email" className="form-control" id="exampleInputEmail" name="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder={iterator.email} required />
                                            </div>
                                            <div className="mb-3">
                                                <label htmlFor="phoneInput" className="form-label">Phone</label>
                                                <input type="text" className="form-control" id="exampleInputPhone" name="phone" value={phone} onChange={(event) => setPhone(event.target.value)} placeholder={iterator.phone} required />
                                            </div>
                                            <div className="mb-3">
                                                <label htmlFor="AddressInput" className="form-label">Address</label>
                                                <input type="text" className="form-control" id="exampleInputAddress" name="address" value={address} onChange={(event) => setAddress(event.target.value)} placeholder={iterator.address} required />
                                            </div>
                                        </form>
                                    </div>
                                    <div className="modal-footer">
                                    <button onClick={(event) => handleSubmitEdit(event, iterator.id)} type="submit" className="btn btn-primary" data-bs-dismiss="modal">Edit</button>
                                    <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                    </div>
                                    </div>
                                </div>
                                </div>
                        )}
                        <i className="fa fa-trash text-danger pointer" onClick={() => handleDeleteContact(item.id)}></i>
                    </span>
                    <h5 className="card-title mb-3">{item.name}</h5>
                    <p className="card-text text-secondary" >
                        <span className="fa fa-location-dot me-3 "></span>
                        {item.address}
                    </p>
                    <p className="card-text text-secondary">
                        <span className="fa fa-phone me-3 "></span>
                        {item.phone}
                    </p>
                    <p className="card-text text-secondary">
                        <span className="fa fa-envelope me-3"></span>
                        {item.email}
                    </p>
                </div>
            </div>
        </div>
    </div>
        
        )}
        
    </div>
    )
}