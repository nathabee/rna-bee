V0.1.x : initialize 



TO DO in 0.1.x  infrastructure`:

1. **Stabilize the current platform**
 
   * Verify WordPress, `/api/health/`, DRF browsable API, PostgreSQL, Redis, and Celery
   * Add a short backup note for Docker volumes
   * Tag the current state as something like `v0.1.0-infrastructure`




TODO in  **V0.2: create an experiment through REST, generate random RNA sequences in Celery, mutate them, store everything in PostgreSQL, and retrieve the results through Django.**


2. **Create the Django domain model**

   * `Experiment`
   * `Sequence`
   * `Generation`
   * `Mutation`
   * `FoldResult`
   * Keep the first model deliberately small
   * Add Django Admin for inspection

3. **Build the first REST endpoints**

   * `POST /api/experiments/`
   * `GET /api/experiments/{id}/`
   * `GET /api/experiments/{id}/results/`
   * `POST /api/sequences/random/`
   * Add OpenAPI/Swagger documentation

4. **Implement the first scientific functionality without folding**

   * Generate random RNA from `A U G C`
   * Parameter `N` for sequence length
   * Add random seed for reproducibility
   * Add single-point mutation
   * Store parent/child sequence relationship
   * Unit tests for generator and mutation logic

5. **Connect Celery properly**

   * Django creates an experiment
   * Django submits a Celery task
   * Worker changes status:
     `PENDING -> RUNNING -> COMPLETED / FAILED`
   * Save results to PostgreSQL
   * Make job errors visible through the API

6. **Integrate ViennaRNA**

   * Install ViennaRNA only in the scientific worker image
   * Implement `ViennaRNAEngine`
   * Input: RNA sequence
   * Output: predicted secondary structure + free energy
   * Store engine/version with every result
   * Add a simple test sequence

7. **Run our first real experiment**
   Start intentionally small:

   ```text
   N = 10
   population = 100 or 1,000
   ```

   For every random sequence:

   * predict structure
   * record ΔG
   * create one point mutation
   * fold mutant
   * compare original vs mutant

   First research question:

   > How much does a single nucleotide mutation change predicted RNA structure and free energy?

8. **Add experiment statistics**

   * ΔG before/after mutation
   * ΔΔG
   * proportion of mutations that preserve structure
   * proportion causing structural change
   * sequence diversity
   * reproducibility using random seed

9. **Build the WordPress frontend**
   The plugin should remain only a REST client.

   * Experiment form
   * Sequence length
   * population size
   * mutations
   * start simulation button
   * progress/status
   * result cards
   * charts
   * link to raw API data

10. **Add RNAstructure as the second engine**
    Only after ViennaRNA works reliably.
    Then we can run:

    ```text
    same sequence
       -> ViennaRNA
       -> RNAstructure
       -> compare predictions
    ```

11. **Evolution phase**
    This comes later:

    * populations
    * reproduction
    * mutation rates
    * generations
    * selection criteria
    * structural robustness
    * biologically motivated fitness measures

12. **Research-quality improvements**

    * experiment export JSON/CSV
    * software/library versions stored with results
    * deterministic seeds
    * tests
    * provenance
    * result deletion/retention strategy
    * backups
    * documentation of model assumptions and limitations

 


 