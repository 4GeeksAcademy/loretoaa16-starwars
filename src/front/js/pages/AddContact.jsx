import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext.js";

export const AddContact = () => {
    const [name, setName] = useState("");
    const [phone, setPhone] = useState("");
    const [email, setEmail] = useState("");
    const [address,setAddress] = useState("");
    const { actions } = useContext(Context);
    const navigate = useNavigate();

    const handleSubmitAdd = (event) => {
        event.preventDefault();
        const dataToSend = {name, phone, email, address};
        actions.addContact(dataToSend)
        navigate("/contact-List");
    }

    return (
        <form className="container" onSubmit={handleSubmitAdd}>
            <div className="mb-3">
                <label htmlFor="FullName" className="form-label">Full Name</label>
                <input type="text" className="form-control" id="exampleFullName" name="name" value={name} onChange={(event) => setName(event.target.value)} placeholder="Full Name" required />
            </div>
            <div className="mb-3">
                <label htmlFor="exampleInputEmail1" className="form-label">Email address</label>
                <input type="email" className="form-control" id="exampleInputEmail" name="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Enter email" required />
            </div>
            <div className="mb-3">
                <label htmlFor="phoneInput" className="form-label">Phone</label>
                <input type="text" className="form-control" id="exampleInputPhone" name="phone" value={phone} onChange={(event) => setPhone(event.target.value)} placeholder="Enter phone" required />
            </div>
            <div className="mb-3">
                <label htmlFor="AddressInput" className="form-label">Address</label>
                <input type="text" className="form-control" id="exampleInputAddress" name="address" value={address} onChange={(event) => setAddress(event.target.value)} placeholder="Enter address" required />
            </div>
            <button type="submit" className="btn btn-primary">Save</button>
        </form>
    );
}