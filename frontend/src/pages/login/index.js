import { Card, Box } from "@mui/material"
import { Lock } from "@mui/icons-material"
import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google"
import axios from "axios"

export default function Login() {
    const onSuccess = async (response) => {
        try{
            document.cookie = `credential=${response.credential}; path=/`;
            console.log("Google response: ",response);

            // const decoded_token = jwtDecode(response.credential);
            // print(decoded_token)

            const res = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND_URL}/user/login`, {
              headers:{
                Authorization: response.credential,
              },
            })

            console.log(res.data)
          }
          catch(err){
            console.log("Google Error2: ",err)
          }
    }

    const onFailure = (response) => {
        console.log(response)
    }

    return (
        <Box height="100vh" sx={{display: "flex", justifyContent: "center", alignItems: "center"}}>
            <Card sx={{maxHeight: "75vh", maxWidth: "85vw", minHeight: "75vh", minWidth: "85vw"}}>
                <div>
                    {/* <!-- component --> */}
                    <div className="bg-zinc-700 flex justify-center items-center h-screen">
                        {/* <!-- Left: Image --> */}
                        <div className="w-1/2 h-screen hidden lg:block">
                            <img src="/chatting.jpg" alt="Placeholder Image" className="object-cover w-full h-full" />
                        </div>
                        <div className="w-1/2 h-screen hidden lg:block">
                            <Box height="75%" width="100%" sx={{display: "flex", justifyContent: "center", alignItems: "center", flexDirection: "column"}}>
                                <Lock sx={{color: "white", margin: "2rem"}} fontSize="large"/>
                                <GoogleOAuthProvider clientId={process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID}>
                                    <GoogleLogin onSuccess={onSuccess} onFailure={onFailure} shape="pill" />
                                </GoogleOAuthProvider>
                            </Box>
                        </div>
                    </div>
                </div>
            </Card>
        </Box>
    )
}
