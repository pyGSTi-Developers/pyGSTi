o
    u�f�"  �                   @   s�   d Z ddlZddlZddlmZ ddlmZ	 ddl
mZ ddlmZ ddlmZ ddlmZ dd	lmZ G d
d� dejej�ZdS )z#
Defines the ParityCheckInst class
�    N)�modelmember)�
operations)�
statespace)�matrixtools)�Label)�reportables)�optoolsc                   @   sj   e Zd ZdZddd�Zdd� Zddd�Zedd� �Zddd�Z	edd� �Z
edd� �Zdd� Zdd� ZdS )�ParityCheckInsta  
    A new class for representing a quantum instrument, the mathematical description 
    of an intermediate measurement. This class relies on the "auxiliary picture" where 
    a n-qubit m-outcome intermediate measurement corresponds to a circuit diagram with
    n plus m auxiliary qubits. 

    Using this picture allows us to extract error generators corresponding to the circuit
    diagram and lays the ground work for a CPTPLND parameterization. 

    Parameters
    ----------
    member_ops : dict of LinearOperator objects
        A dict (or list of key,value pairs) of the gates.
    evotype : Evotype or str, optional
        The evolution type.  If `None`, the evotype is inferred
        from the first instrument member.  If `len(member_ops) == 0` in this case,
        an error is raised.

    state_space : StateSpace, optional
        The state space for this POVM.  If `None`, the space is inferred
        from the first instrument member.  If `len(member_ops) == 0` in this case,
        an error is raised.

    items : list or dict, optional
        Initial values.  This should only be used internally in de-serialization.
    �defaultN�CPTPLNDc           
   	   C   s�  || _ dt�d� t�dgdgdgdgg� }dt�d� t�dgdgdgdgg� }t�t�g d�g d�g d�g d�g��}d	}t�|t�d
��t�t�d
�|� t�|t�d
�� | _t	j
jt�|d
 |d
 f�| j d�| _|d u ryt�|�}t�t�|�|j�t�t�|�|j�g| _| jt�t�|�|� | _g }t	�| j�| _td�D ]}	|�d|	� �t	�| j|	 | j��  | j �g� q�tj�| |� tj�| ||� | ��  | jj| _d S )N�   �   r   �����)r   r   r   r   )r   r   r   r   )r   r   r   r   )r   r   r   r   �   �   ��parameterization�p) r   �_np�sqrt�array�_ot�unitary_to_pauligate�kron�identity�	aux_GATES�_op�LindbladErrorgen�from_error_generator�zeros�	error_gen�_statespace�default_space_for_dim�T�left_isometry�right_isometry�ExpErrorgenOp�	noise_map�range�append�StaticArbitraryOp�to_dense�_collections�OrderedDict�__init__�_mm�ModelMember�init_gpindices�
_paramlbls)
�self�evotype�state_space�itemsr   �zero�one�CNOT�dim�i� r<   �H/Users/pcwysoc/pyGSTi/pygsti/modelmembers/instruments/paritycheckinst.pyr.   4   s&   (((8&
*2zParityCheckInst.__init__c                 C   s
   | j �� S )z�
        Gives the underlying vector of parameters. 

        Returns
        -------
        numpy array
            a 1D numpy array with length == num_params().
        )r    �	to_vector�r3   r<   r<   r=   r>   U   s   
	zParityCheckInst.to_vectorFTc                 C   s\   | j �|� t�| j �| _td�D ]}t�| j| | j��  | j	 �| d|� �< q|| _
dS )a  
        Initialize the Instrument using a vector of its parameters.

        Parameters
        ----------
        v : numpy array
            The 1D vector of gate parameters.  Length
            must == num_params().

        close : bool, optional
            Whether `v` is close to this Instrument's current
            set of parameters.  Under some circumstances, when this
            is true this call can be completed more quickly.

        dirty_value : bool, optional
            The value to set this object's "dirty flag" to before exiting this
            call.  This is passed as an argument so it can be updated *recursively*.
            Leave this set to `True` unless you know what you're doing.

        Returns
        -------
        None
        r   r   N)r    �from_vectorr   r&   r'   r(   r*   r$   r+   r%   �dirty)r3   �v�close�dirty_valuer;   r<   r<   r=   r@   `   s
   ,
zParityCheckInst.from_vectorc                 C   �   | j jS )z�
        Get the number of independent parameters which specify this Instrument.

        Returns
        -------
        int
            the number of independent parameters.
        )r    �
num_paramsr?   r<   r<   r=   rF   ~   �   
zParityCheckInst.num_params� c                 C   sp   t �� }t|t�r!| �� D ]\}}||t|jd | |j�< q|S |r'|d7 }| �� D ]
\}}|||| < q+|S )a[  
        Creates a dictionary of simplified instrument operations.

        Returns a dictionary of operations that belong to the Instrument's parent
        `Model` - that is, whose `gpindices` are set to all or a subset of
        this instruments's gpindices.  These are used internally within
        computations involving the parent `Model`.

        Parameters
        ----------
        prefix : str
            A string, usually identitying this instrument, which may be used
            to prefix the simplified gate keys.

        Returns
        -------
        OrderedDict of Gates
        �_)r,   r-   �
isinstance�_Labelr6   �name�sslbls)r3   �prefix�
simplified�k�gr<   r<   r=   �simplify_operations�   s   
�z#ParityCheckInst.simplify_operationsc                 C   rE   )z�
        Get the labels of the independent parameters which specify this instrument. 
    
        Returns
        -------
        array
            array of parameter labels 
        )r    �parameter_labelsr?   r<   r<   r=   rS   �   rG   z ParityCheckInst.parameter_labelsc                 C   s   t dd� | �� D ��S )a(  
        Return the number of total gate elements in this instrument.

        This is in general different from the number of *parameters*,
        which are the number of free variables used to generate all of
        the matrix *elements*.

        Returns
        -------
        int
        c                 S   s   g | ]}|j �qS r<   )�size)�.0rQ   r<   r<   r=   �
<listcomp>�   s    z0ParityCheckInst.num_elements.<locals>.<listcomp>)�sum�valuesr?   r<   r<   r=   �num_elements�   s   zParityCheckInst.num_elementsc              	   C   s�   |j }|j}t�t�|t�d��| j��  | j	 t�|t�d�� | j	 �| _tj
j| j| jd�| _td�D ]}t�| j| | j��  | j �| d|� �< q6d| _dS )a�  
        Update each Instrument element matrix `O` with `inv(s) * O * s`
        and update the error generator/noise map appropriately.  

        Parameters
        ----------
        s : GaugeGroupElement
            A gauge group element which specifies the "s" matrix
            (and it's inverse) used in the above similarity transform.

        Returns
        -------
        None
        r   r   r   r   TN)�transform_matrix�transform_matrix_inverser   �FullTPOpr   r   �eyer'   r+   r   r   �from_operation_matrixr   r    r(   r*   r$   r%   rA   )r3   �s�Smx�Sir;   r<   r<   r=   �transform_inplace�   s   B,
z!ParityCheckInst.transform_inplacec              	   C   s:   d}| � � D ]\}}|d|tj|�� ddd�f 7 }q|S )NzKParityCheckInstrument representing a two-qubit parity check with elements:
z%s:
%s
r   �   )�width�prec)r6   �_mt�mx_to_stringr+   )r3   r_   �lbl�elementr<   r<   r=   �__str__�   s   "zParityCheckInst.__str__)r
   NNr   )FT)rH   )�__name__�
__module__�__qualname__�__doc__r.   r>   r@   �propertyrF   rR   rS   rY   rb   rj   r<   r<   r<   r=   r	      s    
!




r	   )rn   �collectionsr,   �numpyr   �pygsti.modelmembersr   r/   r   r   �pygsti.baseobjsr   r!   �pygsti.toolsr   rf   �pygsti.baseobjs.labelr   rK   �pygsti.reportr   �_rpr   r   r0   r-   r	   r<   r<   r<   r=   �<module>   s    