<template>
    <v-container class="about-container" align="start">
        <v-row class="description">
            <v-col cols="12">
                <h2>Hi! This is HyperFetch </h2>
                <h3>Smart and environmentally concious</h3>
            </v-col>
        </v-row>

        <v-row class="case main-section rounded">
            <v-col cols="4">
                <div class="card-container">
                    <div class="card mix-4">
                        <h4>Fast</h4>
                        <hr>
                        <br>
                        <span class="link-arrow">⟶</span> <a class="a2" href="https://vitejs.dev/">Vue + Vite</a>
                        <br>
                        <span class="link-arrow">⟶</span> <a class="a2" href="https://fastapi.tiangolo.com/">FastAPI</a>
                        <br>
                        <span class="link-arrow">⟶</span> <a class="a2" href="https://www.mongodb.com/">MongoDB</a>
                        <br>
			        </div>
                </div>
            </v-col>
            <v-col cols="4">
                <div class="card-container">
                    <div class="card mix-4">
                        <h4>Easy to use</h4>
                        <hr>
                        <p>Pip-package abstracts away difficulties of tuning hyperparameters </p>
                    </div>
                </div>
            </v-col>
            <v-col cols="4">
                <div class="card-container">
                    <div class="card mix-4">
                        <h4> Eco-Concious </h4>
                        <hr>
                        <p> Tracks CO2 emissions using hardware and local electricity-grid</p>
			        </div>
                </div>
            </v-col>
        </v-row>
        
        <v-row class="case blue main-section"> 
            <v-col>
                <div class="image-container ">
                    <img src="../assets/about/co2.jpg" alt="CO2 reduction">
                </div>
                <div class="text box-right">
                    <h2>HyperFetch aims to reduce collective emissions</h2>
                    <p>Machine learning models are growing increasingly powerful in their abilities, whether that might be in processing natural language, tackling the intricacies of computer vision, or any other number of exciting applications that are emerging.</p>
                    <p>Training these huge models, howerver, comes at a great cost to the environment. When repetitive training runs are demanded due to the tuning of hyperparameters in addition to that, the collective CO2-emissions are astounding.
                    <p>Hardware and training time has everything to say when calculating CO2 emissions. A research paper named 
                        <a class="small" href="https://arxiv.org/pdf/1906.02243.pdf">Energy and Policy Considerations for Deep Learning in NLP</a>
                        states that an NLP model using Neural Architecture Search can emit 626,000 pounds of CO₂ or more. </p>
                        <br><br>
                        When calculating the CO2 emissions for a full day of training using an RTX 3080 (
                            <a class="small" href="https://mlco2.github.io/impact/#compute">mlco2</a>
                        ) the total emissions are only 7.5 pounds. 
                        However, this application proposes the idea that training only has to happen for new problems. When sharing optimized hyperparameters for an environment such that others can reuse them, aquiring good hyperparameters much more environmentally friendly. 
                        <br>
                        Read more about 
                        <a class="small" href="https://www.nature.com/articles/s42256-022-00529-w">Machine learning's environmental impact<span class="link-arrow">⟶</span></a>
                    </p>
                </div>
            </v-col>
        </v-row>

        <v-row class="case blue main-section">
            <v-col>
                <div class="image-container ">
				    <img src="../assets/about/hurdle.webp" alt="Tuning hyperparameters is very important for output of good model parameters">			
                </div>
                <div class="text box-right">
                    <h2>HyperFetch terminates a big hurdle within RL</h2>
                    <p> Reinforcement learning (RL) with its many components and vast amount of blackboxing can be very hard to understand for those just entering the field. 
                    <br><br>
                    Considering the combinatory problem that is tuning the hyperparameters of a RL model, 
                    the field is very advanced. For those with little to no experience with RL, tuning is an impossible landscape
                    with a numerous amount of pitfall and no with no obvious source of guidance regarding which values to give the hyperparameters. 
                    HyperFetch aims to make the introduction to Reinforcement Learning softer, as beginners will have a two-in-one service. On one side, 
                    HyperFetch will help in tuning hyperparameters for the practicioner. In addition, HyperFetch will supply readily availabe hyper-parameters
                    provided by other pracitcioners in this free and easy to use website. 
                    <br><br>
                    Ready, Fetch, Go!
                </p>
                </div>
            </v-col>
        </v-row>

        <v-row class="case blue main-section"> 
            <v-col>
                <div class="image-container ">
                    <img src="../assets/about/keyboard.gif">
                </div>
                <div class="text box-right">
                    <h2>For researchers: HyperFetch aims to increase reproductability</h2>
                    <p> Without hyperparameters it can be next to impossible to reproduce other projects' results -especially when those projects are performed with great amounts of processing power. 
                        <br><br>
                        Being able to reproduce reinforcement learning (RL) tasks is important to ensure that the research on 
                        the field is reproductuctible such that algorithms/solutions can be compared easily and fairly with minimal bias.
                        As reinforcement learning (RL) is able to solve increasingly complex tasks and problems, however, reproducing
                        results also gets more complex due to the variance of the algorithms, the stochasticity of the environments, and
                        the many hyper-parameters. In addititon, these hyper-parameters are not always published alongside its research (or even at all).
                        Read more in 
                        <a class="small" href="https://arxiv.org/abs/1909.03772">this research paper</a>.
                        To join in on solving the replication crisis in AI, HyperFetch aims to aid in persisting hyper-parameters. For now, hyper-parameters
                        are not linked to specific projects, but are ranked in order of best to least reward. 
                        We aim to make the line between real breakthrough and product showcase less fuzzy. 
                        <br><br>
                        Read more about the replication crisis at: 
                        <a class="small" href="https://www.technologyreview.com/2020/11/12/1011944/artificial-intelligence-replication-crisis-science-big-tech-google-deepmind-facebook-openai/">technologyreview.com <span class="link-arrow">⟶</span></a>

                    </p>
                </div>
            </v-col>
        </v-row>

        <v-row class="main-section dependencies">
            <v-col> 
                <div class="description">
                    <h2>The application relies on:</h2>
                </div>

                <div class="image-container right">
				    <img src="../assets/about/dependencies.webp" alt="The dependencies of the application">			
                </div>
                <div class="card-container">
                    <div class="card-long mix-1">
                        <h4>Optuna </h4>
                        <p> Optuna is a hyperparameter optimization framework with a great trade-off between runtime and performance score. 
                            To read about the how's and why's, read the
                            <a href="https://arxiv.org/pdf/2201.06433.pdf"> comparative study </a>
                            or visit the 
                            <a href="https://optuna.readthedocs.io/en/stable/">Optuna docs</a>.
                        </p>
			        </div>
                    <div class="card-long mix-2">
                        <h4>Stable-Baselines3</h4>
                        <p> Stable-Baselines3 is a set of reliable implementations of reinforcement learning algorithms in PyTorch.
                            You can read more at the 
                            <a href="https://stable-baselines3.readthedocs.io/en/master/">SB3 docs </a>
                        </p>
			        </div>
                    <div class="card-long mix-3">
                        <h4>CodeCarbon</h4>
                        <p> CodeCarbon is a lightweight software package stimates the amount of carbon dioxide (CO2) produced by the cloud or personal computing resources used to execute code. 
                            You can read more about the initiative at the 
                            <a href="https://codecarbon.io/#about">CodeCarbon </a> website.
                        </p>
			        </div>
                </div>
            </v-col>
        </v-row>

        <v-row class="footer">
            <v-col>
                <v-btn @click="toHome" variant="outlined" color="white" elevation="20">Fetch hyperparameters</v-btn>
            </v-col>
            <v-col>
                <v-btn @click="toGetStarted" variant="outlined" color="white" elevation="20">Create hyperparameters</v-btn>
            </v-col>
        </v-row>

    </v-container>
</template>

<script>
import LandingPage from '@/views/LandingPage.vue'
import GetStarted from '@/views/GetStarted.vue'

export default {
    name: "About",

    methods: {
        toGetStarted() {
            this.$router.push({
                  name: 'GetStarted',
                  component: GetStarted,
        })
        },
        toHome() {
            this.$router.push({
                  name: 'Home',
                  component: LandingPage,
        })
        },
    }
}
</script>

<style lang="scss" scoped>
.about-container {

    h2 {
        @media (min-width: 900px) {
            font-size: 48px;
        }
        
        font-weight: 600;
        font-size: 36px;
        line-height: 109.12%;
    }

    h3 {
        @media (min-width: 900px) {
            font-size: 28px;
        }
    
        font-weight: 600;
        font-size: 26px;
        line-height: 109.12%;
    }

    .description {
        text-align: left;
        width: 330px;
        color: #33373d;
        margin: 10px 10px 10px 10px;

        @media (min-width: 900px) {
            width: 850px;
            margin: 70px 40px 60px 25px;
        }

        h2 {
        font-size: 30px;
            @media (min-width: 900px) {
                font-size: 36px;
            }
        }
    }

    .dependencies {
        margin-top: -5vh;
    }

    .right {
        float:right;
    }

    .main-section {
        text-align: left;
        margin-bottom: 80px;

        @media (min-width: 900px) {
            margin-bottom: 100px
        }
        
        .card-container {
            margin-top: 8vh;
            margin-left: 40px;

            h4 {
                font-style: normal;
                font-weight: 600;
                font-size: 24px;
                line-height: 26px;
            }

            p {
                margin-top: 20px;
                line-height: 25px;
                font-size: 16px;
            }

            a {
                text-decoration: none;
                color: #f0885d;
                font-weight: 600;
                font-size: 18px;
                line-height: 25px;
            }

            .card {
                border-radius: 8px;
                width: 50%;
            }
            .card-long {
                margin:  30px 30px 30px 30px;
                padding: 10px 10px 10px 10px;
                border-radius: 8px;
                width: 50%;
            }
            .mix-1 {
                background-color: #454d60;
                color: white;
            }

            .mix-2 {
                background-color: #fbdacb;
                color: black;
            }
                
            .mix-3 {
                background-color: #f3f7ff;
                color: rgb(71, 69, 190);
            }
            .mix-4 {
                width: 60%;
                height: 200px;
                background-color: #8c9eff;
                color: rgb(0, 0, 0);
            }
        }

        .small {
                font-weight: 400 !important;
                line-height: 20px !important;
                font-size: 16px !important;
                text-decoration: none;
                }
                a.small:hover {
                color: #c56339;
                font-weight: 700;
            }
        .case {
            max-width: 1240px;
            margin: 0 auto;
            margin-bottom: 0px;

            .text {
                padding: 25px;
                @media(min-width: 900px) {
                    width: 70%;
                    padding: 50px;
                }
            }

            .blue {
            margin-bottom: 80px;
            }
        }
    }
}

.case.blue .text {
    transform: translateY(-40px);
    background: #5c7e65;
    color: #fdf1eb;
    @media(min-width: 900px) {
        transform: translateY(-15%);
    }
}

.case.blue .image-container {
    padding-left: 5px;
    max-height: 375px;
    @media(min-width: 900px) {
        margin-left: auto;
        margin-right: 10%;
        width: 80%;
    }
    img {
        width: 65%;
        object-fit: cover;

        @media(min-width: 900px) {
            max-height: 75vh;
            border-radius: 5px;
        }
    }
}
@keyframes a1 {
    0% {
         margin-left: 2px;
    }
    50% {
        margin-left: 10px;
    }
    100% {
        margin-left: 2px;
    }
}
.link-arrow {
        animation-name: a1;
        animation-duration: 1s;
        animation-iteration-count: infinite;
        animation-timing-function: ease-in-out;
        font-size: 24px;
        line-height: 28px;
        margin-left: 15px;
        position: absolute;
        @media(min-width: 900px) {
            font-size: 24px;
            line-height: 28px;
            margin-left: 15px;
        }
    }

.case.peach .text {
    transform: translateY(-60px);
    background: #fbdacb;

    @media(min-width: 900px) {
        transform: translateY(-60%);
        margin-left: auto;
        margin-right: 0;
    }
}

body .box-right {
    padding: 50px 50px 50px 50px;
    width: 70%;
    margin-top: 30px;
    border-radius: 5px 0 0 5px;
    margin-left: auto;
    @media(min-width: 900px) {
        border-radius: 5px;
    }
}

.a2 {
    margin-left: 50px;
    color: #9d3810 !important;
}

body a {
    color: #f0885d;
    font-weight: 900;
    font-size: 22px;
    line-height: 30px;

    a:hover {
            color: #c56339;
            font-weight: 700;
    }
}
.footer {
    color:white;
    text-align: center;
    width: 330px;
    margin: 30px 10px 10px 10px;
    padding-bottom: 50px;

    @media (min-width: 900px) {
        width: 600px;
        margin: auto;
    }
}
</style>