const getState = ({ getStore, getActions, setStore,useState }) => {
	const host = "https://playground.4geeks.com/contact";
	const base = "https://www.swapi.tech/api";
	const slug = "loretoaa16";

	return {
		store: {
			selectedItem: {},
			category: "",
			contacts: [],
			characters: [],
			planets: [],
			vehicles: [],
			starships: [],
			favorites: [],
			posts: [],
			user: "",
			isLogged: false,
			isAdmin: false,
			alert: {text:'', visible: false, background: 'primary' },

				},
			

		actions: {
			// Use getActions to call a function within a fuction
			setUser: (newUser) => {setStore({ user: newUser})},
			setAlert: (newAlert) => {setStore({ alert: newAlert})},
			setIsLogged: (value) => {setStore({ isLogged: value})},
			setIsAdmin: (value) => {setStore({ isAdmin: value})},
			login: async (dataToSend) => {
				const uri = `${process.env.BACKEND_URL}/api/login`;
				console.log("soy la uri de login", uri);
				const options = {
					method: 'POST',
					headers: {
						"Content-Type": "Application/json"
					},
					body: JSON.stringify(dataToSend)
				};
				const response = await fetch (uri, options)
				console.log("soy response", response)
				if(!response.ok) {
					console.log('Error login:', response.status, response.statusText)
					return
				}
				const data = await response.json();
				console.log("salio todo bien", data);
				setStore({
					user: data.results,
					isAdmin: data.results.is_admin,
					isLogged: true,
					alert: {text: data.message, visible: true, background: 'success'},
				})
				localStorage.setItem('token', data.access_token)
				localStorage.setItem('user', JSON.stringify(data.results))
				console.log("está logeado", getStore().isLogged)
			},
			isUserLogged: () => {
				const data = JSON.parse(localStorage.getItem('user'))
				console.log(data);

				if (data) {
					setStore({
					user: data.first_name,
					isAdmin: data.is_admin,
					isLogged: true,
					})
				}
			},
			logout: () => {
				localStorage.removeItem('token');
				localStorage.removeItem('user');
				//volver el store a valores de no logeado( user, is logged, is adim , alert)
				getActions().setAlert({text:'', visible: false, background: 'primary'});
				setStore({
					user: '',
					isLogged: false,
					isAdmin: false,
					alert: {text: "User left!", visible: true, background: 'danger'},
				})
			},
			register: async (dataToSend) => {
				const uri = `${process.env.BACKEND_URL}/api/users`;
				console.log("soy la uri de register", uri);
				const options = {
					method: 'POST',
					headers: {
						"Content-Type": "Application/json"
					},
					body: JSON.stringify(dataToSend)
				};
				const response = await fetch (uri, options)
				console.log("soy response de register", response)
				if(!response.ok) {
					console.log('Error registering:', response.status, response.statusText)
					return
				}
				const data = await response.json();
				console.log("el register de salio todo bien", data);
				setStore({
					user: data.results,
					isAdmin: data.results.is_admin,
					isLogged: true,
					alert: {text: data.message, visible: true, background: 'success'},
				})
				localStorage.setItem('token', data.access_token)
				localStorage.setItem('user', JSON.stringify(data.results))
				console.log("estoy registrado", getStore().isLogged)
			},
			getPost: async (postId) => {
				const token = localStorage.getItem('token');
				const uri = `${process.env.BACKEND_URL}/api/posts/${postId}`;
				const options = {
					method: 'GET',
					headers: {
						Authorization: `Berear ${token}`
					}
				}
				const response = await fetch(uri, options)
			},
			updatePost:async (postId, dataToSend) => {
				const token = localStorage.getItem('token');
				const uri = `${process.env.BACKEND_URL}/api/posts/${postId}`;
				const options = {
					method: 'PUT',
					headers: {
						Authorization: `Berear ${token}`,
						"Content-Type": 'application/json'
					},
					body: JSON.stringify(dataToSend)
				}
				const response = await fetch(uri, options)
				if (!response.ok){
					console.log(response.status);
					return
				}
				const data = await response.json()
				console.log(data);
			},
			getUser: async (userId) => {
				const token = localStorage.getItem('token');
				const uri = `${process.env.BACKEND_URL}/api/users/${userId}`;
				const options = {
					method: 'GET',
					headers: { 
						Authorization: `Bearer ${token}`,
						"Content-Type": "application/json"
					},
					body: JSON.stringify(dataToSend) 
				};

				const response = await fetch(uri, options);
				if (!response.ok) {
					console.error('Error getting profile', response.status, response.statusText);
					return;
				}
			
				const data = await response.json();
				console.log("Profile ok:", data);
			},
			updateProfile: async (userId) => {
				const token = localStorage.getItem('token');
				const uri = `${process.env.BACKEND_URL}/api/users/${userId}`;
				const options = {
					method: 'PUT',
					headers: { 
						Authorization: `Bearer ${token}`,
						"Content-Type": "application/json"
					},
					body: JSON.stringify() 
				};
			
				const response = await fetch(uri, options);
				if (!response.ok) {
					console.error('Error editing profile', response.status, response.statusText);
					return;
				}
			
				const data = await response.json();
				console.log("Profile edited:", data);
			},
			setCategory: (cat) => {
			setStore({category: cat})
			},
			setSelectedItem: (category, uid) => {
                fetch(`${base}/${category}/${uid}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.result) {
                            setStore({ selectedItem: data.result.properties });
                        } else {
                            console.error("Invalid response from API", data);
                        }
                    })
                    .catch(error => console.error("Error fetching details:", error));

		
            },
			getCharacters: async() => {
				const store = getStore();
				const uri = `${base}/people/`;
				const options = {
					method:'GET'}
				const response = await fetch (uri, options)
				if(!response.ok) {
					console.log('Error getting characters:', response.status, response.statusText)
					return
				}
				const data = await response.json();
				setStore({characters: data.results})
				console.log(data);
			},
			getVehicles: async() => {
				const store = getStore();
				const uri = `${base}/vehicles/`;
				const options = {
					method:'GET'}
				const response = await fetch (uri, options)
				if(!response.ok) {
					console.log('Error getting vehicles:', response.status, response.statusText)
					return
				}
				const data = await response.json();
				setStore({vehicles: data.results})
				console.log(data);
			},
			getStarships: async() => {
				const store = getStore();
				const uri = `${base}/starships/`;
				const options = {
					method:'GET'}
				const response = await fetch (uri, options)
				if(!response.ok) {
					console.log('Error getting starships:', response.status, response.statusText)
					return
				}
				const data = await response.json();
				setStore({starships: data.results})
				console.log(data);
			},
			getPlanets: async() => {
				const store = getStore();
				const uri = `${base}/planets/`;
				const options = {
					method:'GET'}
				const response = await fetch (uri, options)
				if(!response.ok) {
					console.log('Error getting planets:', response.status, response.statusText)
					return
				}
				const data = await response.json();
				setStore({planets: data.results})
				console.log(data);
			},
			addFavorite: (item) => {
				const store = getStore();
				if (!store.favorites.some(fav => fav.name === item.name)) {
					setStore({ favorites: [...store.favorites, item] });
					console.log(getStore().favorites)
				}
			},
			removeFavorite: (item) => {
				const store = getStore();
				setStore({ favorites: store.favorites.filter(fav => fav.name !== item.name) });
			},
			getContacts: async() =>{
				const uri = `${host}/agendas/${slug}/contacts`;
				const response = await fetch (uri)
				if(!response.ok) {
					console.log('Error get contacts:', response.status, response.statusText)
					return
				}
				const data = await response.json();
				console.log(data);
				setStore({contacts: data.contacts})
			},
			deleteContact: async (id) => {
				const uri = `${host}/agendas/${slug}/contacts/${id}`;
				
				const options = {
					method: 'DELETE',
					headers: { "Content-Type": "application/json" }, 
				};
				console.log(uri, options);

				const response = await fetch(uri, options);
				if (!response.ok) {
					console.error('Error deleting contact', response.status, response.statusText);
					return;
				}
			
				const data = await response.json();
				console.log("Contact deleted:", data);
				getActions().getContacts();
				
			},
			addContact: async (dataToSend) => {
				const uri = `${host}/agendas/${slug}/contacts`;
				
				const options = {
					method: 'POST',
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify(dataToSend) 
				};
				console.log(uri, options);

				const response = await fetch(uri, options);
				if (!response.ok) {
					console.error('Error posting new contact', response.status, response.statusText);
					return;
				}
			
				const data = await response.json();
				console.log("Contact added:", data);
				getActions().getContacts(); 
				
			},	
			editContact: async (id, dataToSend) => {
				const uri = `${host}/agendas/${slug}/contacts/${id}`;
				const options = {
					method: 'PUT',
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify(dataToSend) 
				};
			
				const response = await fetch(uri, options);
				if (!response.ok) {
					console.error('Error editing contact', response.status, response.statusText);
					return;
				}
			
				const data = await response.json();
				console.log("Contact edited:", data);
				setStore()
				getActions().getContacts(); 
			}
			
		}
	};
};

export default getState;
