import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { useNavigate } from "react-router-dom";

export const Login = () => {
    const { actions } = useContext(Context);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [viewPassword, setViewPassword] = useState(false);
    const navigate = useNavigate()

    const handleEmail = (event) => {setEmail(event.target.value)}
    const handlePassword = (event) => {setPassword(event.target.value)}
    const handleViewPassword = () => {setViewPassword(!viewPassword)}

    const handleSubmit = (event) => {
        event.preventDefault();
        const dataToSend = {email, password}
        console.log(dataToSend)
        //asignar el valor de user para darle la bienvenida
        actions.login(dataToSend);
       
        navigate('/')
        // cambien el valor del btn login a logout del navbar
    }

    useEffect(() => {
            actions.login();
                
                }, [navigate]);

    return (
        <main className="form-lognin d-flex justify-content-center align-items-center p-4">
            <form onSubmit={handleSubmit}>
                <h1 className="h3 mb-3 fw-normal text-center">Please Login</h1>
                <div className="form-floating mb-3">
                <input type="email" className="form-control" id="floatingInput" placeholder="Input your email" value={email} onChange={handleEmail}/>
                <label htmlFor="floatingInput">Email address</label>
                </div>
                <div className="input-group mb-4 form-floating">
                    <input type={viewPassword ? 'text' : 'password'} className="form-control" id="floatingPassword" placeholder="Password" value={password} onChange={handlePassword}/>
                    <label htmlFor="floatingPassword">Password</label>
                    <span className="input-group-text" onClick={handleViewPassword}>
                        { viewPassword ? 
                        <i className="fa fa-eye-slash"></i>
                        :
                        <i className="fa fa-eye"></i>
                        }
                    </span>
                </div>
                <button className="btn btn-primary w-100 py-2 p-4" type="submit">Log in</button>
                <div className="text-center mt-3">
                    <span>No tienes cuenta? </span>
                    <a onClick={() => navigate("/register")} href="#">Register</a>
                </div>
            </form>
            </main>
    );
};
