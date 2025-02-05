import React from "react";
import { Link } from "react-router-dom";

export const Navbar = () => {
	return (
		<nav className="navbar navbar-expand-lg bg-body-tertiary">
			<div className="container-fluid">
				<Link to='/' className="navbar-brand">Website</Link>
				<button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
				<span className="navbar-toggler-icon"></span>
				</button>
				<div className="collapse navbar-collapse" id="navbarSupportedContent">
				<ul className="navbar-nav me-auto mb-2 mb-lg-0">
					<li className="nav-item">
					<Link to='/home' className="nav-link">Home</Link>
					</li>
					<li className="nav-item">
					<Link to='/Contact-List' className="nav-link">Contact List</Link>
					</li>
				</ul>
				</div>
				<Link to='/Add-Contact' className="btn btn-primary text-light">Add Contact</Link>
			</div>
		</nav>
	);
};
