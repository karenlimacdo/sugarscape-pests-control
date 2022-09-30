amostras_controladas_pelo_vento_0 <- todas_as_amostras[todas_as_amostras$vento==0,]
unique(amostras_controladas_pelo_vento_0$`Lagarta Saudavel`)
[1] 100   0   1   3   2   4   7   6   5
faixas_de_corte <- c(0, 3, 7, 100)
bact50 <- Freq(amostras_controladas_pelo_vento_0$`Lagarta Saudavel`[amostras_controladas_pelo_vento_0$initial_population_bt==50],breaks = faixas_de_corte)
bact100 <- Freq(amostras_controladas_pelo_vento_0$`Lagarta Saudavel`[amostras_controladas_pelo_vento_0$initial_population_bt==100],breaks = faixas_de_corte)
bact150 <- Freq(amostras_controladas_pelo_vento_0$`Lagarta Saudavel`[amostras_controladas_pelo_vento_0$initial_population_bt==150],breaks = faixas_de_corte)
bact200 <- Freq(amostras_controladas_pelo_vento_0$`Lagarta Saudavel`[amostras_controladas_pelo_vento_0$initial_population_bt==200],breaks = faixas_de_corte)
crosstable <- as.table(rbind(bact50$freq, bact100$freq, bact150$freq, bact200$freq))
crosstable
    A   B   C
A 188  12   0
B 196   4   0
C 200   0   0
D 199   1   0
dimnames(crosstable) <- list(pop_ini_bact=c("Baixa","Media","Alta","Maxima"),pop_fim_lag=c("Baixa","Média","Alta"))
crosstable
            pop_fim_lag
pop_ini_bact Baixa Média Alta
      Baixa    188    12    0
      Media    196     4    0
      Alta     200     0    0
      Maxima   199     1    0
chisq.test(crosstable)

Pearson's Chi-squared test

data:  crosstable
X-squared = NaN, df = 6, p-value = NA

Warning message:
In chisq.test(crosstable) :
  Aproximação do qui-quadrado pode estar incorreta
