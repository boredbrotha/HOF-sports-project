import {Link} from 'react-router-dom'


function Verify(){


    return(
        <div className = "verify-root">

            <h1 className="verification-line">We just sent you a verification email. After you're done, click the link below to log-in.</h1>
            <Link to = "/login">Log-In</Link>
        </div>
    )
}

export default Verify;