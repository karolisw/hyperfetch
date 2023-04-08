<template>
    <v-container class="about-container" align="center">
        <v-row class="header">
            <v-col cols="12">
                <h2>Hi! This is HyperFetch </h2>
                <h3>Smart and environmentally concious</h3>

            </v-col>
        </v-row>

        <v-row class="case main-section intro rounded">
            <v-col cols="4">
                <div class="card-container">
                    <div class="card mix-4">
                        <h4>Fast</h4>
                        <br>
                        <span class="link-arrow">⟶</span> <a target="_blank" href="https://vitejs.dev/">Vue + Vite</a>
                        <br>
                        <span class="link-arrow">⟶</span> <a target="_blank" href="https://fastapi.tiangolo.com/">FastAPI</a>
                        <br>
                        <span class="link-arrow">⟶</span> <a target="_blank" href="https://www.mongodb.com/">MongoDB</a>
                        <br>
			        </div>
                </div>
            </v-col>
            <v-col cols="4">
                <div class="card-container">
                    <div class="card mix-4">
                        <h4>Easy to use</h4>
                        <p>Pip-package abstracts away difficulties of tuning hyperparameters </p>
                    </div>
                </div>
            </v-col>
            <v-col cols="4">
                <div class="card-container">
                    <div class="card mix-4">
                        <h4> Eco-Concious </h4>
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
                    <p> Training machine learning models in themselves is very energy-intensive. When repetitive training runs are demanded due to the tuning of hyperparameters in addition to that, the collective CO2-emissions are astounding.
                        <br><br>
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Obcaecati iste corporis adipisci id! Deserunt voluptates dignissimos ipsum, maxime exercitationem dolorem blanditiis atque corrupti nihil rem eos, aperiam a adipisci tempore sit eligendi provident perferendis sapiente! Ipsam quam repellat delectus fuga, doloribus libero eum, praesentium laborum voluptatem veritatis cupiditate, quod veniam in vitae eveniet omnis id itaque quasi beatae alias distinctio! Rerum libero placeat reiciendis pariatur dolor eum quisquam quos in nisi dolorum tempore, minima error aut repellendus cum, maxime accusamus natus ex amet deleniti distinctio exercitationem. Officiis eum tempore corrupti beatae ipsa. Eligendi dicta officia natus sequi nesciunt enim earum?
                    </p>
                    <a target="_blank" href="https://www.nature.com/articles/s42256-022-00529-w">nature.com<span class="link-arrow">⟶</span></a>
                </div>
            </v-col>
        </v-row>

        <v-row class="case blue main-section">
            <v-col>
                <div class="image-container ">
				    <img src="../assets/about/hurdle.webp" alt="Tuning hyperparameters is very important for output of good model parameters">			
                </div>
                <div class="text box-left">
                    <h2>HyperFetch terminates a big hurdle within RL</h2>
                    <p> Reinforcement learning (RL) with its many components and vast amount of blackboxing can be very hard to understand for those just entering the field. 
                    <br><br>
                    Considering the combinatory problem that is tuning the hyperparameters of a RL model, the field is very advanced without help in tuning them.</p>
                </div>
            </v-col>
        </v-row>

        <v-row class="case peach main-section"> 
            <v-col>
                <div class="video-container ">
                    <img src="../assets/about/keyboard.gif">
                </div>
                <div class="text box-left">
                    <h2>For researchers: HyperFetch aims to increase reproductability</h2>
                    <p> Without hyperparameters it can be next to impossible to reproduce other projects' results -especially when those projects are performed with great amounts of processing power. 
                        <br><br>
                        Vi har vært med å utvikle hele den tekniske platformen til FeltGIS, og vi har utforsket mange spennende idéer og teknologier på vei mot den endelige tekniske løsningen.
                        AI is suffering a replication crisis where "...the line between real breakthrough and product showcase can be fuzzy."
                    </p>
                    <a target="_blank" href="https://www.technologyreview.com/2020/11/12/1011944/artificial-intelligence-replication-crisis-science-big-tech-google-deepmind-facebook-openai/">technologyreview.com <span class="link-arrow">⟶</span></a>
                </div>
            </v-col>
        </v-row>

        <v-row class="main-section dependencies">
            <v-col>
                <div class="image-container right">
				    <img src="../assets/about/dependencies.webp" alt="The dependencies of the application">			
                </div>
                <div class="card-container">
                    <h2>The application relies on:</h2>
                    <div class="card mix-1">
                        <h4>Optuna </h4>
                        <p> Optuna is a hyperparameter optimization framework with a great trade-off between runtime and performance score. 
                            To read about the how's and why's, read the
                            <a href="https://arxiv.org/pdf/2201.06433.pdf"> comparative study </a>
                            or visit the 
                            <a href="https://optuna.readthedocs.io/en/stable/">Optuna docs</a>.
                        </p>
			        </div>
                    <div class="card mix-2">
                        <h4>Stable-Baselines3</h4>
                        <p> Stable-Baselines3 is a set of reliable implementations of reinforcement learning algorithms in PyTorch.
                            You can read more at the 
                            <a href="https://stable-baselines3.readthedocs.io/en/master/">SB3 docs </a>
                        </p>
			        </div>
                    <div class="card mix-3">
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
                <v-btn @click="toUsingPip" variant="outlined" color="white" elevation="20">Create hyperparameters</v-btn>
            </v-col>
        </v-row>

    </v-container>
</template>

<script>
import LandingPage from './LandingPage.vue'
import UsingPip from './UsingPip.vue'

export default {
    name: "About",

    methods: {
        toUsingPip() {
            this.$router.push({
                  name: 'UsingPip',
                  component: UsingPip,
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

    @media (min-width: 900px) {
        margin: auto;
    }

    h2 {
        @media (min-width: 900px) {
            font-size: 48px;
        }
        
        font-weight: 900;
        font-size: 36px;
        line-height: 109.12%;
    }

    h3 {
        @media (min-width: 900px) {
            font-size: 28px;
        }
    
        font-weight: 900;
        font-size: 26px;
        line-height: 109.12%;
    }

    .header {
        text-align: center;
        width: 330px;
        color: #33373d;
        margin: 10px 10px 10px 10px;

        @media (min-width: 900px) {
            width: 850px;
            margin: 40px 40px 40px 40px;
        }

        h2 {
        font-size: 30px;
            @media (min-width: 900px) {
                font-size: 36px;
            }
        }
    }

    .intro {
        background: #4745be78;
    }

    .dependencies {
        margin-top: -185px;
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

            h4 {
                font-style: normal;
                font-weight: 800;
                font-size: 24px;
                line-height: 26px;
            }

            p {
                margin-top: 16px;
                margin-bottom: 16px
            }

            a {
                text-decoration: none;
                color: #f0885d;
                font-weight: 900;
                font-size: 18px;
                line-height: 30px;
            }

            .card {
                box-shadow: 0 3px 6px rgba(174, 174, 174, 0.678),0 3px 6px rgba(174, 174, 174, 0.64);
                padding: 20px;
                border-radius: 8px;
                margin: 15px;
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
                width: 200px;
                height: 200px;
                background-color: #ffffff;
                color: rgb(71, 69, 190);
            }
        }
        .case {
            max-width: 1240px;
            margin: 0 auto;
            margin-bottom: 0px;
            
            .image-container {
                width: 70%;
                @media(min-width: 900px) {
                    margin: 0 auto;
                    margin-right: auto;
                    margin-left: auto;
                    width: 80%;
                }
            }

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

            .video-container {
                border-radius: 5px 0 0 5px;
                max-width: 50%;
                @media(min-width: 900px) {
                    transform: translateY(0);
                    width: 100%;
                    border-radius: 5px;
                }
            }
        }
    }
}

.case.blue .text {
    transform: translateY(-40px);
    background: #33373d;
    color: #fdf1eb;
    @media(min-width: 900px) {
        transform: translateY(-20%);
    }
}

.case.blue .image-container {
    padding-left: 5px;
    max-height: 375px;
    @media(min-width: 900px) {
        margin-left: auto;
        margin-right: 5%;
        width: 80%;
    }
    .background {
        background-color: #fdf1eb;
    }
    img {
        width: 60%;
        object-fit: cover;

        @media(min-width: 900px) {
            max-height: 75vh;
            border-radius: 5px;
        }
    }
}

.link-arrow {
  animation-name: example;
  animation-duration: 1s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
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

body .box-left {
    padding: 50px 50px 50px 50px;
    width: 70%;
    margin-top: 30px;
    border-radius: 0 5px 5px 0;
    margin-right: auto;
    @media(min-width: 900px) {
        border-radius: 5px;
    }
}

body a {
    color: #f0885d;
    font-weight: 900;
    font-size: 22px;
    line-height: 30px;

    .link-arrow {
        font-size: 22px;
        line-height: 24px;
        margin-left: 20px;
        position: absolute;
        @media(min-width: 900px) {
            font-size: 24px;
            line-height: 28px;
            margin-left: 15px;
        }
    }
}
.footer {
    color:white;
    text-align: center;
    width: 330px;
    margin: 30px 10px 10px 10px;
    padding-bottom: 150px;

    @media (min-width: 900px) {
        width: 600px;
        margin: auto;
    }
}

</style>