import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext.js";

export const Navbar = () => {
	 const { store, actions } = useContext(Context);  

	return (
		<nav className="navbar navbar-expand-lg bg-body-tertiary bg-dark" data-bs-theme="dark">
			<div className="container-fluid">
				<Link to='/' className="navbar-brand">Star Wars</Link>
				<button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
				<span className="navbar-toggler-icon"></span>
				</button>
				<div className="collapse navbar-collapse" id="navbarSupportedContent">
				<ul className="navbar-nav me-auto mb-2 mb-lg-0">
					<li className="nav-item">
					<Link to='/contact-List' className="nav-link">Contact List</Link>
					</li>
					<li className="nav-item">
					<Link to='/characters' className="nav-link">Characters</Link>
					</li>
					<li className="nav-item">
					<Link to='/vehicles' className="nav-link">Vehicles</Link>
					</li>
					<li className="nav-item">
					<Link to='/starships' className="nav-link">Starships</Link>
					</li>
					<li className="nav-item">
					<Link to='/planets' className="nav-link">Planets</Link>
					</li>
				</ul>
				</div>
				<div className="btn-group" role="group">
					<button id="btnGroupDrop1" type="button" className="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
					<i className="fa fa-heart text-light pointer"></i>
					</button>
					<ul className="dropdown-menu dropdown-menu-end" aria-labelledby="btnGroupDrop1">
					{store.favorites.map((item) => 
					<li key={item.id}><Link className="dropdown-item" to='/planets'>{item.name}</Link><i className="fa fa-delete text-danger pointer" onClick={() => actions.removeFavorites(item)}></i></li>
					)}
					</ul>
				</div>
			</div>
		</nav>
	);
};
	