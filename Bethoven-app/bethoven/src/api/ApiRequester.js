import store from '@/store';
import Axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
// import { ILogin } from "./ILogin";
// import { IRegister } from './IRegister';
// import { IToudoumResponse } from './IToudoumResponse';
// import { ToudoumError } from './ToudoumError';
// import { ToudoumError422 } from './ToudoumError422';

/**
 * API Service to link Front-End and Back-End
 * Allow developer to contact an APi with a Singleton pattern
 * 
 * @class ApiRequester
 */
class ApiRequester {
    // Properties
    static singleton;
    instanceAxios;
    token;
    URL = "http://localhost:8000/";
    client_id = "dhVqxxKFZYhvItVvOOU2KtD6EnKJYERcjcvdq8Kh";
    client_secret = "VaBmlKbzvDtVwDkyzUzcQa6nMU8osXQnLg1D21B859TR2IronyqWGRRPtjUouhSywKx3lEsDD5f33bYr2p9rbKrCesws3G0kHm3oEl02VtWSMyS2uPqZ1x7cGB7CjMit";
    grant_type = "password";

    /**
     * Creates an instance of ApiRequester.
     */
    constructor() {
        this.token = null;
        this.instanceAxios = Axios.create({
            baseURL: `${this.URL}api/`,
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });
    }

    /**
     * Get Url
     *
     * @return {*} 
     */
    getUrl() {
        return this.URL;
    }

    /**
     * Get ApiRequester Instance (or create it if inexistant)
     *
     * @readonly
     * @static
     * @type {ApiRequester}
     */
    static get instance() {
        if (!ApiRequester.singleton) {
            this.singleton = new ApiRequester();
        }
        return ApiRequester.singleton;
    }

    setToken(token) {
        this.token = token;
    }

    /**
     * Log User in Application and store his token
     *
     * @param {ILogin} credentials credentials to log
     * @return {*}  {Promise<IToudoumResponse>} API Response
     */
    async login(credentials) {
        try {

            var bodyFormData = new FormData();
            bodyFormData.append("grant_type", this.grant_type);
            bodyFormData.append(
                "client_id",
                this.client_id
            );
            bodyFormData.append(
                "client_secret",
                this.client_secret
            );
            bodyFormData.append("username", credentials.username);
            bodyFormData.append("password", credentials.password);

            //TO REMOVE
            console.log(bodyFormData);

            const response = await this.instanceAxios.post("login/token/", bodyFormData);
            console.log(response.data);

            this.token = response.data.access_token;

            // Store user in Vuex store and sessionStorage
            store.dispatch('logUser', this.token);
            window.sessionStorage.setItem("user", credentials.username);
            window.sessionStorage.setItem("token", this.token);
            return response.data;
        } catch (error) {
            const data = error.response.data;
            if (data.data == undefined) {
                //throw new ToudoumError(data.code, data.message, data.status);
            } else {
                //throw new ToudoumError422(data.code, data.message, data.status, data.data);
            }
        }
    }

    async logout() {
        store.dispatch('logout');
        window.sessionStorage.removeItem("user");
        window.sessionStorage.removeItem("token");
        // const response = await this.get("logout");
        this.token = null;
        // return response;
    }

    /**
     * Register an Account
     *
     * @param {IRegister} account account to register
     * @return {*}  {Promise<AxiosResponse>} API Response
     */
    async register(account) {
        try {
            const response = await this.instanceAxios.post("users/", {
                "username": account.username,
                "password": account.password,
                "email": account.email
            });
            this.login({ "username": account.username, "password": account.password });
            return response;

        } catch (error) {
            throw error.response.data;
            if (data.data == undefined) {
                // throw new ToudoumError(data.code, data.message, data.status);
            } else {
                // throw new ToudoumError422(data.code, data.message, data.status, data.data);
            }
        }
    }

    /**
     * Check if API server is UP
     *
     * @return {*}  {Promise<AxiosResponse>} API Response
     */
    getStateServer() {
        return this.instanceAxios.get("state");
    }


    /**
     * Request a GET Method
     *
     * @template T type to cast the data got from API
     * @param {string} url url to request 
     * @return {*}  {Promise<T>} Promise of type T
     */
    async get(url) {
        try {
            const response = await this.instanceAxios.get(url, {
                headers: { Authorization: `Bearer ${this.token}` }
            });
            return response.data;
        } catch (error) {
            throw error.response.data;
            // if (data.data == undefined) {
            //     throw new ToudoumError(data.code, data.message, data.status);
            // } else {
            //     throw new ToudoumError422(data.code, data.message, data.status, data.data);
            // }
        }
    }

    /**
     * Request the API
     *
     * @private
     * @param {("GET" | "POST" | "PUT" | "DELETE" | "PATCH")} method string method to use
     * @param {string} url url to request
     * @param {*} [body] body to add in request
     * @return {*}  {Promise<IToudoumResponse>} Api Response
     */
    async request(method, url, body = null) {

        const requestConfig = {
            method: method,
            url: url,
            headers: { Authorization: `Bearer ${this.token}`, }
        };


        if (body != null) {
            requestConfig.data = body;
        }

        try {
            const response = await this.instanceAxios(requestConfig);
            return response.data;
        } catch (error) {
            throw error.response.data;
            // if (data.data == undefined) {
            //     // throw new ToudoumError(data.code, data.message, data.status);
            // } else {
            //     // throw new ToudoumError422(data.code, data.message, data.status, data.data);
            // }
        }
    }



    /**
     * POST data to API
     *
     * @param {string} url url to request
     * @param {*} body body to post
     * @return {*}  {Promise<IToudoumResponse>} API Response
     */
    async post(url, body) {
        return this.request("POST", url, body);
    }

    /**
     * PUT data to API
     *
     * @param {string} url url to request
     * @param {*} body body to put
     * @return {*}  {Promise<IToudoumResponse>} API Response
     */
    async put(url, body) {
        return this.request("PUT", url, body);
    }

    /**
     * DELETE method to API
     *
     * @param {string} url url to request
     * @return {*}  {Promise<IToudoumResponse>} API Response
     */
    delete(url) {
        return this.request("DELETE", url);
    }

    /**
     * PATCH method to API
     *
     * @param {string} url url to request
     * @param {*} body body to PATCH
     * @return {*}  {Promise<IToudoumResponse>} API Response
     */
    async patch(url, body) {
        return this.request("PATCH", url, body);
    }

    async formData(url, body) {
        const requestConfig = {
            method: "POST",
            url: url,
            headers: {
                Authorization: `Bearer ${this.token}`,
                "Content-Type": "multipart/form-data"
            }
        };


        if (body) {
            requestConfig.data = body;
        }

        try {
            const response = await this.instanceAxios(requestConfig);
            return response.data;
        } catch (error) {
            throw error.response.data;
            // if (data.data == undefined) {
            //     throw new ToudoumError(data.code, data.message, data.status);
            // } else {
            //     throw new ToudoumError422(data.code, data.message, data.status, data.data);
            // }
        }
    }

}

export default ApiRequester.instance;