import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import { useNavigate } from "react-router-dom";

export const Register = () => {
    const { store, actions } = useContext(Context);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [viewPassword, setViewPassword] = useState(false);
    const navigate = useNavigate()
    
    const handleFirstName = (event) => {setFirstName(event.target.value)}
    const handleLastName = (event) => {setLastName(event.target.value)}
    const handleEmail = (event) => {setEmail(event.target.value)}
    const handlePassword = (event) => {setPassword(event.target.value)}
    const handleViewPassword = () => {setViewPassword(!viewPassword)}

    const handleSubmit = (event) => {
        event.preventDefault();
        const dataToSend = {
            first_name: firstName, 
            last_name: lastName, 
            email: email, 
            password: password
        }
        console.log(dataToSend)
        //asignar el valor de user para darle la bienvenida
        actions.register(dataToSend);
       
        navigate('/')
        // cambien el valor del btn login a logout del navbar
    }

    return (
        <main className="form-register w-100 m-auto">
            <form onSubmit={handleSubmit}>
                <h1 className="h3 mb-3 fw-normal">Please Register</h1>
                <div className="form-floating">
                <input type="text" className="form-control" id="floatingInput" placeholder="enter your first name" value={firstName} onChange={handleFirstName}/>
                <label htmlFor="floatingInput">First Name</label>
                </div>
                <div className="form-floating">
                <input type="text" className="form-control" id="floatingInput" placeholder="enter your last name" value={lastName} onChange={handleLastName}/>
                <label htmlFor="floatingInput">Last Name</label>
                </div>
                <div className="form-floating">
                <input type="email" className="form-control" id="floatingInput" placeholder="name@example.com" value={email} onChange={handleEmail}/>
                <label htmlFor="floatingInput">Email address</label>
                </div>
                <div className="form-floating">
                <input type={viewPassword ? 'text' : 'password'}  className="form-control" id="floatingPassword" placeholder="Password" value={password} onChange={handlePassword}/>
                <label htmlFor="floatingPassword">Password</label>
                <span className="input-group-text" onClick={handleViewPassword}>
                        { viewPassword ? 
                        <i className="fa fa-eye-slash"></i>
                        :
                        <i className="fa fa-eye"></i>
                        }
                    </span>
                </div>

        
                <button className="btn btn-primary w-100 py-2" type="submit">Register</button>
                <div className="text-center mt-3">
                    <span>Ya tienes cuenta? </span>
                    <a onClick={() => navigate("/login")} href="#">Log in</a>
                </div>
            </form>
            </main>
    );
};
