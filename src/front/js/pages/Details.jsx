import React, { useContext } from "react";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import {Link} from "react-router-dom";
import { Context } from "../store/appContext.js";


export const Details = () => {
    const { store, actions } = useContext(Context); 

    return (
      <div className="row featurette">
        <div className="col-md-7 order-md-2">
          <h1 className="text-center">{store.selectedItem.name || store.selectedItem.title}</h1>
          <h2 className="featurette-heading">Oh yeah, it’s that good. <span class="text-muted">See for yourself.</span></h2>
          <p className="lead">{store.selectedItem.description || "No description available"}</p>
          <ul>
                {Object.keys(store.selectedItem).map((key, index) => (
                    <li key={index}>
                        <strong>{key}:</strong> {store.selectedItem[key]}
                    </li>
                ))}
            </ul>
        </div>
        <div className="col-md-5 order-md-1">
          <svg className="bd-placeholder-img bd-placeholder-img-lg featurette-image img-fluid mx-auto" width="500" height="500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder: 500x500" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="#eee"></rect><text x="50%" y="50%" fill="#aaa" dy=".3em">500x500</text></svg>
  
        </div>
      </div>
    )
}

