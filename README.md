# Stream Cipher - Ejercicio en clase

## Análisis de Seguridad
- **¿Qué sucede cuando cambia la clave utilizada para generar el keystream?** La clave utilizada es la base del algoritmo para generar números pseudoaleatorios, cuando la clave cambia se genera un keystream distinto. Esto hace que la seguridad del cifrado dependa directamente de la clave utilizada. Veamos el ejemplo:
```
og_message = "Hello, World!"
key_seed = 3
keystream = keystream_random(3, len(encrypted_text))

key_seed = 6
keystream = keystream_random(6, len(encrypted_text))
```

- **¿Qué riesgos de seguridad existen si reutiliza el mismo keystream para cifrar dos mensajes diferentes?** Asumiendo que los dos mensajes tienen el mismo tamaño y el keystream es exactamente el mismo, cifrar dos mensajes diferentes permite al atacante usar XOR entre los mensajes. Al hacerlo, el keystream se cancela y se obtiene el XOR de los mensajes originales. Esto permite extraer información parcial de los mensajes, lo cual es especialmente peligroso cuando el atacante conoce parcialmente alguno de los mensajes porque puede fácilmente obtener el otro. Ejemplo del ataque: 
```
msg1 = "HOLA MUNDO"
msg2 = "HOLA MARIA"

key = 5

c1 = encrypt(msg1, key)
c2 = encrypt(msg2, key)

leak = bytes([a ^ b for a, b in zip(c1, c2)])

print(leak)
```
![Resultado de XOR entre cifrados](resultados_ejemplo/xor_entre_cifrados.png)


- **¿Cómo afecta la longitud del keystream a la seguridad del cifrado?** Un keystream más corto que el mensaje genera patrones, al repetirse, que pueden ser detectados por un atacante. Cuando el keystream tiene la misma longitud que el mensaje, cada byte del texto plano se combina con un valor diferente, lo cual proporciona mayor seguridad. Y si el keystream es más largo que el mensaje, la seguridad no se ve afectada, sin embargo, se desperdician recursos computacionales. Así que lo ideal es generar un keystream del mismo tamaño que el mensaje.

- **¿Qué consideraciones debe tener al generar un keystream en un entorno de producción real?** 
1. El generador de números pseudoaleatorios debe ser criptográficamente seguro. El módulo `random` de python no está diseñado para fines de seguridad, por lo que debe sustituirse por librerías especializadas.
2. Se debe evitar la reutilización del keystream. Para ello, normalmente se emplean valores aleatorios adicionales, como nonces o vectores de inicialización, que garantizan secuencias únicas en cada cifrado.
3. Se deben proteger adecuadamente las claves, evitando almacenarlas en el código fuente o en repositorios públicos.
4. Es vital incluir autenticación e integridad de datos, porque el cifrado por sí solo no impide que un atacante modifique los mensajes.

## Validación y pruebas
A continuación se muestran tres ejemplos de cifrado y descifrado usando el stream cipher implementado:
![Resultados de ejemplos de entrada/salida](resultados_ejemplo/entrada_salida.png)

Adicionalmente se realizaron pruebas unitarias para validar que:
- El descifrado recupera exactamente el mensaje original
- Diferentes claves producen diferentes textos cifrados
- La misma clave produce el mismo texto cifrado (determinismo)
- El cifrado maneja correctamente mensajes de diferentes longitudes

## Reflexión Técnica
1. **Limitaciones de PRNG Simples**

Existen limitantes importantes en los PRNG simples, como el utilizado en esta implementación mediante el módulo `random`. Para empezar, son predictivos, si el atacante obtiene la semilla o parte de la secuencia generada, puede reconstruir el resto del keystream. Además, cada cierto rango se repiten las secuencias, su periodicidad juega en contra porque los patrones son detectados y explotados. Lamentablemente no son de alta calidad estadística, quiere decir que, aunque los valores parezcan aleatorios a simple vista, pueden presentar correlaciones o distribuciones no uniformes. Esto facilita ataques basados en análisis estadístico y hace que el cifrado sea vulnerable.

2. **Comparación con Stream Ciphers Modernos**

Los stream ciphers modernos, como ChaCha20 y AES en modo CTR, generan keystreams utilizando algoritmos diseñados específicamente para ofrecer alta seguridad criptográfica. Estos algoritmos han sido analizados ampliamente por la comunidad científica.

Ofrecen una alta resistencia a la predicción, incluso si un atacante conoce parte del keystream, no puede calcular los valores siguientes sin conocer la clave secreta. Esto evita ataques basados en reconstrucción de la secuencia. Con el uso de técnicas avanzadas, como funciones criptográficas, operaciones matemáticas complejas y múltiples rondas de transformación, evitan las vulnerabilidades presentes en los generadores simples. Eliminando cualquier tipo de patrones y correlaciones en los datos generados.

En cuanto a la inicialización y el estado interno, los stream ciphers modernos emplean claves, nonces y contadores. Estos son valores que garantizan que cada sesión de cifrado produzca un keystream único, incluso si se reutiliza la misma clave. En comparación, la implementación presentada en este proyecto utiliza únicamente una semilla simple, carece de mecanismos avanzados de inicialización y no protege adecuadamente su estado interno.

3. Referencias
- [D. J. Bernstein. (2008). ChaCha, a variant of Salsa20.](https://www.researchgate.net/publication/229028741_ChaCha_a_variant_of_Salsa20)
- [GeeksforGeeks. (2025, July 15). Stream Ciphers.](https://www.geeksforgeeks.org/computer-networks/stream-ciphers/)
- [Computerphile. (2021, February 19). Chacha Cipher - computerphile [Video]. YouTube.](https://www.youtube.com/watch?v=UeIpq-C-GSA)

## Uso de IA para esta tarea
En esta ocasión tomé la oportunidad de usar un LLM para realizar las pruebas unitarias adecuadas. Tras tener el código con las funciones de stream cypher, lo incluí en el prompt junto con los requerimientos de pruebas y me devolvió el código de Python con las pruebas adecuadas.

Adicionalmente fue de utilidad para revisar preguntas teóricas, mejorar redacción y facilitar la investigación técnica sobre stream ciphers modernos.