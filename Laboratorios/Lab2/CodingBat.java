public int[] zeroFront(int[] nums) {
  boolean [] used = new boolean [nums.length];
  int cont = 0;
  for (int i = 0; i < nums.length; i++) {
    if(nums[i] == 0) {
      if (i != cont) {
        nums[i] = nums[cont];
        nums[cont] = 0;
      }
      cont++;
    }
  }
  return nums;
}

public int[] notAlone(int[] nums, int val) {
  for(int i = 1; i < nums.length-1; i++) {
    if(nums[i] == val && nums[i-1] != val && nums[i+1] != val) {
      if (nums[i-1] > nums[i+1])
        nums[i] = nums[i-1];
      else
        nums[i] = nums[i+1];
    }
  }
  return nums;
}

public int[] post4(int[] nums) {
  int [] nArray = new int[0];
  for(int i = nums.length-1; i >= 0; i--) {
    if(nums[i] == 4) {
      if (i == nums.length-1)
        break;
      else {
        nArray = new int[nums.length - i - 1];
        for (int j = 0; j < nArray.length; j++) {
          nArray[j] = nums[i + j + 1];
        }
        break;
      }
    }
  }
  return nArray;
}

public int[] tenRun(int[] nums) {
  int tempMult = 0;
  boolean used = false;
  for(int i = 0; i < nums.length; i++) {
    if (nums[i]%10 == 0) {
      used = true;
      tempMult = nums[i];
    }
    if(used)
      nums[i] = tempMult;
  }
  return nums;
}

public int[] shiftLeft(int[] nums) {
  int [] mod = new int[nums.length];
  if (nums.length==1) return nums;
  for (int i=1; i<nums.length; i++) {
    mod[nums.length-1]=nums[0];
    mod[i-1]=nums[i];
  }
  return mod;
}
